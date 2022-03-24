from PyQt5 import QtGui, QtCore, QtWidgets

import pyaudio 
import wave
from collections import deque
import os
import time
import math
import GlobalVars
import copy
global graph_win
import pyqtgraph as pg

CHUNK = 8192 #*4

FORMAT = pyaudio.paInt16 #this is the standard wav data format (16bit little endian)s

MAX_DUR=60 #max dur in seconds

def RescanInputs():
    import GlobalVars

   
    inputdevices = 0
    
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    
    
    #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
    for i in range (0,numdevices):
        if p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
            print("DevID ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name'))
            inputdevices+=1

    GlobalVars.numdevices=inputdevices
    p.terminate()


def TriggeredRecordAudio(ui):

 import GlobalVars
 global graph_win1
 global graph_win2
 global graph_win3
 global graph_win4

 from pydub import AudioSegment
 import array
 import pdb
 
 
 RATE = int(ui.SampleRatecomboBox.currentText());# sampling frequency
 MIN_DUR=GlobalVars.buffertime*2+0.1;#

 SILENCE_LIMIT = GlobalVars.buffertime;
 PREV_AUDIO = GlobalVars.buffertime;

 p = pyaudio.PyAudio()

 CHANNELS=GlobalVars.CHANNELS;
 rel = int(RATE/(CHUNK))
 last_val_high = [0] * CHANNELS
 last_val_low = [0] * CHANNELS
 last_data = [0] * CHANNELS
 

 stream=p.open(format=FORMAT,input_device_index=GlobalVars.inputdeviceindex,channels=GlobalVars.CHANNELS,rate=RATE,
               input=True,
               frames_per_buffer=CHUNK)
    
 ui.ListeningTextBox_1.setText('<span style="color:green">quiet</span>')
 ui.ListeningTextBox_2.setText('<span style="color:green">quiet</span>')
 ui.ListeningTextBox_3.setText('<span style="color:green">quiet</span>')
 ui.ListeningTextBox_4.setText('<span style="color:green">quiet</span>')
 
 audio2send1 = [] 
 audio2send2 = []
 audio2send3 = []
 audio2send4 = []
 

 prev_audio1 = deque(maxlen=PREV_AUDIO * rel) #prepend audio running buffer
 prev_audio2 = deque(maxlen=PREV_AUDIO * rel) #prepend audio running buffer
 prev_audio3 = deque(maxlen=PREV_AUDIO * rel) #prepend audio running buffer
 prev_audio4 = deque(maxlen=PREV_AUDIO * rel) #prepend audio running buffer
 
 perm_win1 = deque(maxlen=PREV_AUDIO*rel)
 perm_win2 = deque(maxlen=PREV_AUDIO*rel)
 perm_win3 = deque(maxlen=PREV_AUDIO*rel)
 perm_win4 = deque(maxlen=PREV_AUDIO*rel)


 plot_win1 = deque(maxlen=math.ceil(0.5*rel)) # ! 500ms of display;
 plot_win2 = deque(maxlen=math.ceil(0.5*rel))
 plot_win3 = deque(maxlen=math.ceil(0.5*rel))
 plot_win4 = deque(maxlen=math.ceil(0.5*rel))
 
 started1 = False
 started2 = False
 started3 = False
 started4 = False
 

 def updateGraph():
     if (ui.Ch1checkBox.isChecked()):
         ui.GraphWidgetCh1.plot(plotarray1, width=1, clear=True)
     if (ui.Ch2checkBox.isChecked()):
         ui.GraphWidgetCh2.plot(plotarray2, width=1, clear=True)
     if (ui.Ch3checkBox.isChecked()):
         ui.GraphWidgetCh3.plot(plotarray3, width=1, clear=True)
     if (ui.Ch4checkBox.isChecked()):
         ui.GraphWidgetCh4.plot(plotarray4, width=1, clear=True)
       
 timer = pg.QtCore.QTimer()
 timer.timeout.connect(updateGraph)
 timer.start(1000)
 
 #count=0;

 
 while (GlobalVars.isRunning==1):


  QtWidgets.qApp.processEvents()      
  
  cur_data = stream.read(CHUNK)
  sound = AudioSegment(cur_data, sample_width=pyaudio.get_sample_size(FORMAT), channels=CHANNELS, frame_rate=RATE)

  #sound, last_val_low=low_pass_filter_by_chunk(sound, 15000, last_val_low)
  #sound, last_val_high, last_data=high_pass_filter_by_chunk(sound, int(ui.HighPassspinBox.value()), last_val_high,last_data)
  
  channels = sound.split_to_mono();

  

  if (ui.Ch1checkBox.isChecked()):
      
      ch1=channels[0].raw_data;
    #  pdb.set_trace();
      perm_win1.append(ch1)
      plot_win1.append(ch1)
      data = b''.join(list(plot_win1))
      plotarray1 = array.array("h",data);
      #pdb.set_trace();

      if(sum([x > (GlobalVars.threshold1) for x in plotarray1])>100 and len(audio2send1)<MAX_DUR*rel):  
       if(not started1):
          ui.ListeningTextBox_1.setText('<span style="color:red">singing</span>')
          started1 = True
       audio2send1.append(ch1)
      elif (started1 is True and len(audio2send1)>MIN_DUR*rel):
       print("Ch1 Finished")      
       filename = save_audio(list(prev_audio1) + audio2send1,GlobalVars.Ch1DirPath,GlobalVars.Ch1fileName)
       started1 = False      
       prev_audio1 = copy.copy(perm_win1)
       ui.ListeningTextBox_1.setText('<span style="color:green">quiet</span>')
       audio2send1=[]
      elif (started1 is True):     
       print('Ch1 too short')
       started1 = False       
       prev_audio1 = copy.copy(perm_win1)
       audio2send1=[]
       ui.ListeningTextBox_1.setText('<span style="color:green">quiet</span>')
      else:  
       prev_audio1.append(ch1)

       
  if (ui.Ch2checkBox.isChecked()):

      ch2=channels[1].raw_data;    
      plot_win2.append(ch2)
      perm_win1.append(ch2)
      data = b''.join(list(plot_win2))
      plotarray2 = array.array("h",data); 
      
      if (sum([x > GlobalVars.threshold2 for x in plotarray2])>100 and len(audio2send2)<MAX_DUR*rel):
       if(not started2):
          ui.ListeningTextBox_2.setText('<span style="color:red">singing</span>')
          started2 = True
       audio2send2.append(ch2)
      elif (started2 is True and len(audio2send2)>MIN_DUR*rel):
       print("Ch2 Finished")
       filename = save_audio(list(prev_audio2) + audio2send2,GlobalVars.Ch2DirPath,GlobalVars.Ch2fileName)
       started2 = False       
       prev_audio2 = copy.copy(perm_win2)
       ui.ListeningTextBox_2.setText('<span style="color:green">quiet</span>')
       audio2send2=[]
      elif (started2 is True):
       ui.ListeningTextBox_2.setText('Ch2 too short')
       started2 = False    
       prev_audio2 = copy.copy(perm_win2)
       audio2send2=[]
       ui.ListeningTextBox_2.setText('<span style="color:green">quiet</span>')
      else:
       prev_audio2.append(ch2)

  if (ui.Ch3checkBox.isChecked()):
      ch3=channels[2].raw_data;
      
      plot_win3.append(ch3)       
      perm_win3.append(ch3)
      data = b''.join(list(plot_win3))
      plotarray3 = array.array("h",data);                 
      
      if (sum([x > GlobalVars.threshold3 for x in plotarray3])>100 and len(audio2send3)<MAX_DUR*rel):
       if(not started3):
          ui.ListeningTextBox_3.setText('<span style="color:red">singing</span>')
          started3 = True
       audio2send3.append(ch3)
      elif (started3 is True and len(audio2send3)>MIN_DUR*rel):
       print("Ch3 Finished")
       filename = save_audio(list(prev_audio3) + audio2send3,GlobalVars.Ch3DirPath,GlobalVars.Ch3fileName)
       started3 = False
       slid_win3 = deque(maxlen=SILENCE_LIMIT * rel)
       prev_audio13= copy.copy(perm_win3)
       ui.ListeningTextBox_3.setText('<span style="color:green">quiet</span>')
       audio2send3=[]
      elif (started3 is True):
       ui.ListeningTextBox_3.setText('Ch3 too short')
       started3 = False
       slid_win3 = deque(maxlen=SILENCE_LIMIT * rel)
       prev_audio3 = copy.copy(perm_win3)
       audio2send3=[]
       ui.ListeningTextBox_3.setText('<span style="color:green">quiet</span>')
      else:
       prev_audio3.append(ch3)

      

  if (ui.Ch4checkBox.isChecked()):

      ch4=channels[3].raw_data;
      perm_win4.append(ch4)
      plot_win4.append(ch4)       
      data = b''.join(list(plot_win4))
      plotarray4 = array.array("h",data);       
      
      if (sum([x > GlobalVars.threshold4 for x in plotarray4])>100 and len(audio2send4)<MAX_DUR*rel):
       if(not started4):
          ui.ListeningTextBox_4.setText('<span style="color:red">singing</span>')
          started4 = True
       audio2send4.append(ch4)
      elif (started4 is True and len(audio2send4)>MIN_DUR*rel):
       print("Ch4 Finished")
       filename = save_audio(list(prev_audio4) + audio2send4,GlobalVars.Ch4DirPath,GlobalVars.Ch4fileName)
       started4 = False       
       prev_audio4 = copy.copy(perm_win1)
       ui.ListeningTextBox_4.setText('<span style="color:green">quiet</span>')
       audio2send4=[]
      elif (started4 is True):
       ui.ListeningTextBox_4.setText('Ch4 too short')
       started4 = False       
       prev_audio4 = copy.copy(perm_win4)
       audio2send4=[]
       ui.ListeningTextBox_4.setText('<span style="color:green">quiet</span>')
      else:
       prev_audio4.append(ch4)
              
 print("done recording")
 stream.close()
 p.terminate()

def save_audio(data,rootdir,filename):
 import GlobalVars
 import pdb
 import os
 import pyaudio
 """ Saves mic data to  WAV file. Returns filename of saved
 file """

 # writes data to WAV file

 T=time.localtime()
 RATE=int(GlobalVars.SampleRate);
 
 outtime=str("%02d"%T[0])+str("%02d"%T[1])+str("%02d"%T[2])+str("%02d"%T[3])+str("%02d"%T[4])+str("%02d"%T[5])
 DatePath='/'+str("%02d"%T[0])+'_'+str("%02d"%T[1])+'_'+str("%02d"%T[2])+'/'
 filename = rootdir+DatePath+filename+'_'+outtime

 
 
 if not os.path.exists(os.path.dirname(rootdir+DatePath)):
    try:
        os.makedirs(os.path.dirname(rootdir+DatePath))
    except:
        print('File error- bad directory?')

 
 data = b''.join(data)
        
 wf = wave.open(filename + '.wav', 'wb')
 wf.setnchannels(1);
 wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
 wf.setframerate(RATE) 
 wf.writeframes(data)
 wf.close()
 return filename + '.wav'
 
