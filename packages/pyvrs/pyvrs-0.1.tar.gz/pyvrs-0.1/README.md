# VRS (Voice Recognition Software)

A powerful voice recognition library made in python. This combines several libraries in order to achieve a "Voice Assistant" ready library.

## Features

- Works both offline and offline (Online will utilize the google recognizer from [SpeechRecognitionI](https://pypi.org/project/SpeechRecognition/))

- Realtime speech recognition through the use of  [VOSK](https://alphacephei.com/vosk/)

- Use any wakeword/hotword you want. Some wakewords will utilize [pvporcupine](https://pypi.org/project/pvporcupine/) for better accuracy while some will rely on VOSK's realtime capability.

- Allows for preprocessing before performing **final** recognition (i.e., remove bg noise, increase certain frequencies, etc.) 
