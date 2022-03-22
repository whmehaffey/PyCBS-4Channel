Works w/ Pyton 3.6-10 (PyAudio Suuports up to that). 
python -m pip install --upgrade pip 
python -m pip install pyserial 
python -m pip install numpy 
python -m pip install pyqtgraph
python -m pip install scipy
python -m pip install pydub
python -m pip install pyqt5

Thre are errors from numpy periodically, and it may have to be downgraded to a different version. 



https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
Only the above version of PyAudio will super high channel counts. 

get correct version (e.g. for Python 3.6 and for your system)
pip install filename.whl 


bitdepth is 16 (Make sure your hardware matches, some FocusRites default to 24), and
you can select the freqnency (but has to match what you set the hardware to, this doesn’t change the hardware to this sampling frequency). 

This has only been tested on Win 7 - 11 w/ a Sapphire 4 channel USB audio device

https://focusrite.com/en/usb-audio-interface/scarlett/scarlett-18i8

but should work on any audio device with 4 channels as a single device (e.g. not 4 separate adressable channels). 
