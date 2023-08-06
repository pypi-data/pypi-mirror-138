import asyncio
import json
import threading
import time
import wave
import queue
from dataclasses import dataclass
from typing import Any, Callable, List, Union

import numpy as np
import pvporcupine
import vosk
from maglevapi.basic import quick_kwargs
from pyaudio_mixer import InputTrack
from pyaudio_mixer.utils import BasicFX
from speech_recognition import AudioFile, Recognizer, UnknownValueError
from tensorflow.keras.models import load_model

from .constants import *


@dataclass
class Result:
    """
    Result Types
    ------------
    `active_listening` :
        What is being heard at all times. Text data is written to `payload`.
    `woke` :
        Once the wakeword has been recognized (or .wake_up() has been called manually). Used wakeword is written to `payload`, could be none.
    `error` :
        When an error has been caught. Original exception is written to `exception`.
    `recognized` :
        When the phrase has been fully recognized. Text data is written to `payload`. Audio data is written to `audio_data` as a ndarray.
    `unknown` :
        When the recognized phrase is unknown.
    `realtime_recognition` :
        What the recognizer is currently recognizing (realtime speech recognition). Text data is written to `payload`
    `voice_activity` :
        Whether there is voice activity going on. Probability of a voice activity is written to `payload`
    """

    type: str
    payload: Any = None
    exception: Exception = None
    audio_data: np.ndarray = None

    @property
    def raw_audio_data(self) -> bytes:
        if self.audio_data is None:
            return
        return self.audio_data.tobytes()


class VAD:
    """
    Voice Activity Detection.

    Parameters
    ----------
    `model` : str
        Path to the .h5 file of this voice activity detection model.
    `threshold` : float
        Sensitivity threshold.

    Methods
    -------
    `async def detect(data: bytes)` :
        returns True if the classified data is a voice, otherwise False.
    """

    def __init__(self, model: str, threshold: float = 0.8) -> None:
        self.model = load_model(model)
        self.threshold = threshold

        self.buffer = []

    def format_predictions(self, preds: list) -> list:
        predictions = [[i, float(r)] for i, r in enumerate(preds)]
        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions

    async def detect(self, data: np.ndarray) -> bool:
        data = np.frombuffer(data.tobytes(), dtype="int16")

        # Get the decibel values
        dbs = 20 * np.log10(np.abs(np.fft.rfft(data[:2048])))

        # Collect the decibel values  for the frequencies of interest and round them to 2
        features = list(np.round(dbs[3:VAD_FREQUENCIES], 2))
        self.buffer.append(features)

        if len(self.buffer) == int(SAMPLERATE / CHUNK_SIZE * VAD_DURATION):
            total = np.array([x for y in self.buffer for x in y])
            self.buffer.clear()

            # Make the predictions
            predictions = self.model(np.array([total]))[0]
            predictions = self.format_predictions(predictions)

            idx, prob = predictions[0]
            if idx == 1 and prob >= self.threshold:
                return (True, prob)
        return (False, 0)


class VRS:
    """
    Initializes the VRS (Voice Recognition Software)

    Notes
    -----
    - It is required for you to install nest_asyncio and patch your asyncio via `nest_asyncio.apply()`.

    Parameters
    ----------
    `vad` : VAD
        Voice activity detection class.
    `vosk_path` : str
        Path to the vosk model.
    `input_tracks` : List[InputTrack]
        List of input track to get audio data from.
    `wakewords` : List[str]
        List of wakewords to recognize.
    `callback` : Callable
        Coroutine used to get results.
    `loop` : AbstractEventLoop
        Asyncio event loop.
    `save_path` : str
        Where to save the final file that will be recognized via google speech recognizer. File must be a .wav format (e.g, "temporary_speech.wav")
    `wakeword_sensitivity` : float
        Sensitivity for the wakewords. Defaults to 0.5.
    `logging` : Logger
        Logger object from py-prettylog. Defaults to None. If provided, all logs coming from the VRS will be in a group called "vrs"
    `output_track` : OutputTrack
        If provided, every audio data coming from the input tracks will be redirected here. Defaults to None.
    `disable_vosk` : bool
        Whether to disable the vosk recognizer. Defaults to False.
    `speech_lengths` : Tuple[float, float]
        How many seconds of speech has to occur before cutting off. First tuple represents the initial
    `offline` : bool
        Whether to use the vosk recognizer only (i.e, we're running offline and don't want to send the audio file to google's speech recognition). Defaults to False.
    `google_recognizer_key` : str
        Google speech recognition key. Defaults to None which is the default key the SpeechRecognition package uses.
    `preprocessing_chain` : dict
        Key, Value pair effects where in key is the effect function from the `BasicFX` class and the value must be a dictionary that acts as the parameter to that effect function.
    """

    def __init__(
        self,
        vad: VAD,
        vosk_path: str,
        input_tracks: List[InputTrack],
        wakewords: List[str],
        callback: Callable,
        loop: asyncio.AbstractEventLoop,
        save_path: str,
        **kwargs
    ) -> None:

        # Required Parameters
        self.vad = vad
        self.vosk_path = vosk_path
        self.input_tracks = input_tracks if isinstance(
            input_tracks, list) else [input_tracks]
        self.wakewords = wakewords if isinstance(
            wakewords, list) else [wakewords]
        self._callback = callback
        self.loop = loop
        self.save_path = save_path

        # Kwargs
        self.wakeword_sensitivity, \
            self.logging, \
            self.output_track, \
            self.disable_vosk, \
            self.speech_lengths, \
            self.offline, \
            self.google_recognizer_key, \
            self.preprocessing_chain \
            = quick_kwargs(
                ("wakeword_sensitivity", 0.5),
                ("logging", None),
                ("output_track", None),
                ("disable_vosk", False),
                ("speech_lengths", (6.0, 0.9)),
                ("offline", False),
                ("google_recognizer_key", None),
                ("preprocessing_chain", {}),
                kwargs=kwargs
            )

        # Initialize pvporcupine (accurate wakeword recognizer)
        self.porcupine = None
        if any(kw in pvporcupine.KEYWORDS for kw in self.wakewords):
            _kws = [x for x in self.wakewords if x in pvporcupine.KEYWORDS]
            self.porcupine = pvporcupine.create(
                keywords=_kws,
                sensitivities=[self.wakeword_sensitivity] * len(_kws)
            )
        self.wakewords = set(self.wakewords)

        # Initialize the vosk recognizer (realtime offline speech recognition)
        if not self.disable_vosk:
            self.vosk_model = vosk.Model(self.vosk_path)
        self.vosk = None
        self.restart_vosk()

        # Initialize the speechrecognition module. This module is used for the final speech recognition.
        self.sr_recognizer = Recognizer()

        # Initialize the list of available effects (for preprocessing)
        self.preprocessor = BasicFX(
            dtype=self.input_tracks[0].stream.dtype,
            samplerate=self.input_tracks[0].stream.samplerate
        )
        if self.preprocessing_chain:
            for _e in self.preprocessing_chain.keys():
                if _e not in [x.__name__ for x in self.preprocessor.effects]:
                    raise ValueError(f"unknown effect '{_e}'")

        ######
        self.listen = True
        self.stopped = True
        self.callback_params = {}
        self.q = queue.Queue(maxsize=15)
        self.__woke = False
        self.__stop_signal = False
        self.__last_vosk_reset = time.time()
        self.__to_be_recognized = []
        self.__last_va = None
        self.__last_recognized = time.time()

    def restart_vosk(self) -> None:
        if not self.disable_vosk:
            self.vosk = vosk.KaldiRecognizer(self.vosk_model, SAMPLERATE)

    def read_tracks(self) -> np.ndarray:
        try:
            return self.input_tracks[0].read()
        except AttributeError:

            if self.logging:
                self.logging.warning(
                    "Unknown error 'AttributeError' occurred.", groups=LOGGING_GROUP)

            return

    def reset_variables(self) -> None:
        self.__woke = False
        self.__last_vosk_reset = time.time()
        self.__last_va = None
        self.__to_be_recognized.clear()
        self.callback_params = {}

        if not self.disable_vosk:
            self.vosk.FinalResult()

    def __input_streamer__(self) -> None:
        while not self.__stop_signal:
            data = self.read_tracks()
            if data is not None:
                try:
                    self.q.put(data, block=False)
                except queue.Full:
                    pass

            time.sleep(0.0001)
        
        for _ in range(10):
            try:
                self.q.put(None, block=False)
            except queue.Full:
                pass
    
    def __preprocess_data(self, data: np.ndarray) -> np.ndarray:

        for effect in self.preprocessor.effects:
            params = self.preprocessing_chain.get(effect.__name__)
            if params is not None:
                if effect.__name__ not in ["noise_reduction"] and len(data) > 2048:
                    _buffer = []
                    for d in np.array_split(data, len(data) / 2048):
                        _buffer.append(effect(d, **params))
                    data = np.concatenate(_buffer)
                else:
                    data = effect(data, **params)

        return data

    async def callback(self, *args, **kwargs) -> None:
        await self._callback(*args, **kwargs, **self.callback_params)

    async def start(self) -> None:
        if self.logging:
            self.logging.debug("Starting VRS...", group=LOGGING_GROUP)

        def f():
            self.loop.run_until_complete(self.__vrs__())

        threading.Thread(target=f, daemon=True).start()
        threading.Thread(target=self.__input_streamer__, daemon=True).start()

        if self.logging:
            self.logging.debug(
                "Waiting for VRS to be ready...", group=LOGGING_GROUP)

        while self.stopped:
            await asyncio.sleep(0.001)

        if self.logging:
            self.logging.success(
                "VRS Started successfully.", group=LOGGING_GROUP)

    async def stop(self, blocking: bool = True) -> None:
        if self.logging:
            self.logging.debug("Stopping the VRS...", group=LOGGING_GROUP)
        self.__stop_signal = True

        if blocking:
            while not self.stopped:
                await asyncio.sleep(0.01)

        if self.logging:
            self.logging.success(
                "VRS Stopped successfully", group=LOGGING_GROUP)

    async def wait_for_wakeword(self, data: np.ndarray) -> Union[None, str]:
        wakeword_used = None
        if self.porcupine:
            idx = self.porcupine.process(data)
            if idx > -1:
                wakeword_used = [
                    x for x in self.wakewords if x in pvporcupine.KEYWORDS][idx]

        if not self.disable_vosk:
            _as_bytes = data.tobytes()
            __reset = False
            if len(_as_bytes) != 0:
                self.vosk.AcceptWaveform(_as_bytes)
                __partial = json.loads(self.vosk.PartialResult())

                if __partial["partial"]:
                    await self.callback(Result("active_listening", __partial["partial"]))

                    if len(__partial["partial"].split()) > 25:
                        __reset = True

                if (time.time() - self.__last_vosk_reset) > 30.0:
                    self.__last_vosk_reset = time.time()
                    __reset = True

                if not wakeword_used:
                    ___wakeword = [
                        x for x in self.wakewords if x in __partial["partial"]]
                    if ___wakeword:
                        wakeword_used = ___wakeword[0]

            if __reset:
                self.vosk.FinalResult()
                self.restart_vosk()

        if wakeword_used:
            if not self.disable_vosk:
                self.vosk.FinalResult()

        return wakeword_used

    async def wake_up(self, wakeword: str = None, **kwargs) -> None:
        result = Result("woke", wakeword)
        self.__woke = True

        self.callback_params = kwargs
        await self.callback(result)

    async def fully_recognize(self) -> None:
        self.__last_recognized = time.time()

        if not self.__to_be_recognized:
            return await self.callback(Result("error", exception=ValueError("empty __to_be_recognized variable.")))
        
        preprocessed = self.__preprocess_data(np.concatenate(self.__to_be_recognized))

        # Match data types if they do not match
        if preprocessed.dtype != self.input_tracks[0].stream.dtype:
            preprocessed = preprocessed.astype(self.input_tracks[0].stream.dtype)

        if self.offline:
            if not self.disable_vosk:
                self.vosk.FinalResult()
                self.vosk.AcceptWaveform(preprocessed.tobytes())

                result = Result("recognized", json.loads(
                    self.vosk.FinalResult())["text"], audio_data=preprocessed)
                return await self.callback(result)
            return await self.callback(Result("error", exception=ValueError("vosk should not be disabled if offline is True")))

        # Save the file and recognize it using the SpeechRecognizer library (more accurate since it uses google's)
        itrack = self.input_tracks[0]
        wf = wave.open(self.save_path, "wb")
        wf.setnchannels(itrack.stream.channels)
        wf.setsampwidth(2)
        wf.setframerate(itrack.stream.samplerate)
        wf.writeframes(preprocessed.tobytes())
        wf.close()

        # Convert it into a AudioFile that the SpeechRecognizer module can use
        try:
            with AudioFile(self.save_path) as src:
                audio = self.sr_recognizer.record(src)
        except Exception as e:
            return await self.callback(Result("error", "Error trying to convert the saved file into a AudioFile object.", e))

        # Attempt to recognize using google's recognizer
        try:
            content = self.sr_recognizer.recognize_google(
                audio, key=self.google_recognizer_key)
            r = Result("recognized", content, audio_data=preprocessed)
        except UnknownValueError:
            r = Result("unknown")
        except Exception as e:
            r = Result("error", "Error trying to recognize the audio.", e)
        finally:
            return await self.callback(r)

    async def __vrs__(self) -> None:
        while not self.__stop_signal:
            self.stopped = False
            if not self.listen:
                continue

            data = self.q.get()
            if data is None:
                continue

            # Write the data to the output if it exists. (i.e., we'll here what we're saying)
            if self.output_track:
                self.output_track.write(data, wait=False)

            # 1: Constantly listen until a wakeword has been mentioned
            # A active_listening callback is also constantly being emitted
            if not self.__woke:
                wakeword_used = await self.wait_for_wakeword(data)

                if (time.time() - self.__last_recognized) < 1.8:
                    wakeword_used = None

                if wakeword_used:
                    await self.wake_up(wakeword_used)
                else:
                    continue

            # 2: Wakeword has been said, record until no more voice activity.
            # A realtime_recognition callback is also constantly being emitted
            self.__to_be_recognized.append(data)
            if not self.disable_vosk:
                self.vosk.AcceptWaveform(data.tobytes())
                partial = json.loads(self.vosk.PartialResult()).get("partial")
                if partial:
                    await self.callback(Result("realtime_recognition", partial))

            # 2.1: Listen for voice activities and stop "recording" once there is no more voice activity.
            # A voice_activity callback is also being emitted for every voice activity
            va, prob = await self.vad.detect(data)
            if va:

                if self.__last_va is None:
                    required_length = self.speech_lengths[0]
                else:
                    required_length = self.speech_lengths[1]

                self.__last_va = time.time()
                await self.callback(Result("voice_activity", prob))

            if self.__last_va is not None:
                duration = time.time() - self.__last_va
                if duration > required_length:
                    await self.fully_recognize()
                    self.reset_variables()

        """Code below will only be reached once stop() is called or an exception occurred inside the loop."""
        await asyncio.sleep(0.1)
        self.stopped = True
        self.__stop_signal = False
        self.q.queue.clear()
