from distutils.core import setup

install_requires = [
    "tensorflow==2.6.0",
    "keras==2.6.0",
    "numpy",
    "nest_asyncio",
    "maglevapi",
    "mixer-pyaudio",
    "pvporcupine==1.9.0",
    "SpeechRecognition==3.8.1",
    "vosk==0.3.32",
    "sounddevice==0.4.4",
    "soundfile==0.10.3.post1",
    "py-prettylog",
    "wave"
]

setup(
    name="pyvrs",
    packages=["advanced_vrs"],
    version="0.5",
    license="MIT",
    description="A powerful voice recognition library made in python. This combines several libraries in order to achieve a 'Voice Assistant' ready library.",
    author="Philippe Mathew",
    author_email="philmattdev@gmail.com",
    url="https://github.com/bossauh/pyvrs",
    download_url="https://github.com/bossauh/pyvrs/archive/refs/tags/v_05.tar.gz",
    keywords=["voice", "speech to text", "voice recognition"],
    install_requires=install_requires
)
