
import sys

from PyQt5.QtWidgets import QApplication,QDialog,QSizeGrip
from PyQt5 import QtCore, QtGui, uic, QtWidgets

qtCreatorFile = "GUI2.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

from AudioRecorderFunctions import *
import GlobalVars


def RescanInputsButtonPushed():
    
    import GlobalVars
    import pyaudio 
    import pdb
    
    
    inputdevices = 0
    
    pya = pyaudio.PyAudio()
    info = pya.get_host_api_info_by_index(0)
    DeviceList = info.get('deviceCount')
    ui.InputSelectioncomboBox.disconnect()
    ui.InputSelectioncomboBox.clear();
    ui.InputSelectioncomboBox.currentIndexChanged.connect(InputSelectioncomboBoxChanged)
    
    #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
    for i in range (0,DeviceList):
        #print(pya.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels'))
        if pya.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>1:
            #print(pya.get_device_info_by_host_api_device_index(0,i).get('name'))
            #if ((pya.get_device_info_by_host_api_device_index(0,i).get('name').find("Te"))!=-1):
             ui.InputSelectioncomboBox.insertItem(20,str(pya.get_device_info_by_host_api_device_index(0,i).get('name')))    
             inputdevices+=1
     
  
def StopPushButton():   
    import GlobalVars
    GlobalVars.isRunning=0
    
    ui.StartPushButton.setEnabled(True)
    ui.RescanInputsPushButton.setEnabled(True)
    ui.SampleRatecomboBox.setEnabled(True);
 
    ui.InputSelectioncomboBox.setEnabled(True)
    ui.BufferTimeSpinBox.setEnabled(True)    
    ui.ListeningTextBox.setText('')
    ui.Ch1SaveDirPushButton.setEnabled(True);
    ui.Ch2SaveDirPushButton.setEnabled(True);
    ui.Ch3SaveDirPushButton.setEnabled(True);
    ui.Ch4SaveDirPushButton.setEnabled(True);
    ui.ThresholdLineEdit1.setEnabled(True)
    ui.ThresholdLineEdit2.setEnabled(True)
    ui.ThresholdLineEdit3.setEnabled(True)
    ui.ThresholdLineEdit4.setEnabled(True)    
    
def StartPushButton():

    import GlobalVars
    
    ui.StartPushButton.setEnabled(False)
    ui.RescanInputsPushButton.setEnabled(False)
    ui.SampleRatecomboBox.setEnabled(False);
  
    ui.InputSelectioncomboBox.setEnabled(False)    
    ui.BufferTimeSpinBox.setEnabled(False)
    ui.Ch1SaveDirPushButton.setEnabled(False);
    ui.Ch2SaveDirPushButton.setEnabled(False);
    ui.Ch3SaveDirPushButton.setEnabled(False);
    ui.Ch4SaveDirPushButton.setEnabled(False);
    
    ui.ThresholdLineEdit1.setEnabled(True)
    ui.ThresholdLineEdit2.setEnabled(True)
    ui.ThresholdLineEdit3.setEnabled(True)
    ui.ThresholdLineEdit4.setEnabled(True)
    
    
    GlobalVars.isRunning=1

    TriggeredRecordAudio(ui)
    

def ThresholdLineEditChanged1(newvalue):
    import GlobalVars
    GlobalVars.threshold1=float(newvalue)        
    
def ThresholdLineEditChanged2(newvalue):
    import GlobalVars
    GlobalVars.threshold2=float(newvalue)

def ThresholdLineEditChanged3(newvalue):
    import GlobalVars
    GlobalVars.threshold3=float(newvalue)

def ThresholdLineEditChanged4(newvalue):
    import GlobalVars
    GlobalVars.threshold4=float(newvalue)    
   
def BufferTimeSpinBoxChanged(newvalue):
    import GlobalVars
    GlobalVars.buffertime=int(newvalue)
    
def InputSelectioncomboBoxChanged(newvalue):
    import GlobalVars
    import pyaudio
    import pdb
 
    
    GlobalVars.inputdeviceindex=int(newvalue)    

    p = pyaudio.PyAudio()            
    
    GlobalVars.CHANNELS=p.get_device_info_by_host_api_device_index(0,newvalue).get('maxInputChannels')
      
    devinfo = p.get_device_info_by_index(int(newvalue)) 
       
    samplerates = 32000, 44100, 48000, 96000, 128000
    ui.SampleRatecomboBox.disconnect()
    ui.SampleRatecomboBox.clear();
    
    for fs in samplerates:
        try:            
            p.is_format_supported(fs,  # Sample rate
                         input_device=devinfo['index'],
                         input_channels=devinfo['maxInputChannels'],
                         input_format=pyaudio.paInt16)
        except Exception as e:
            print(fs, e)
        else:            
            ui.SampleRatecomboBox.insertItem(20,str(fs))    
  
    p.terminate
           
    ui.SampleRatecomboBox.setCurrentText(str(GlobalVars.SampleRate))
    ui.SampleRatecomboBox.currentIndexChanged.connect(updateSampleRate);    

   
    ui.Ch1SaveDirPushButton.setEnabled(False);
    ui.Ch2SaveDirPushButton.setEnabled(False);
    ui.Ch3SaveDirPushButton.setEnabled(False);
    ui.Ch4SaveDirPushButton.setEnabled(False);

    ui.Ch1checkBox.setEnabled(False);
    ui.Ch1checkBox.setEnabled(False);
    ui.Ch1checkBox.setEnabled(False);
    ui.Ch1checkBox.setEnabled(False); 


    if (GlobalVars.CHANNELS >0):
        ui.Ch1SaveDirPushButton.setEnabled(True);
        if (GlobalVars.Ch1fileName!=''):
            ui.Ch1checkBox.setEnabled(True);

    if (GlobalVars.CHANNELS >1):
        ui.Ch2SaveDirPushButton.setEnabled(True);
        if (GlobalVars.Ch2fileName!=''):
            ui.Ch2checkBox.setEnabled(True);
    if (GlobalVars.CHANNELS >2):
        ui.Ch3SaveDirPushButton.setEnabled(True);
        if (GlobalVars.Ch3fileName!=''):
            ui.Ch3checkBox.setEnabled(True);
            
    if (GlobalVars.CHANNELS >3):
        ui.Ch4SaveDirPushButton.setEnabled(True);
        if (GlobalVars.Ch4fileName!=''):
            ui.Ch4checkBox.setEnabled(True);                   


    
def Ch1SaveDirPushButtonpushButtonClicked():

    import os
    import GlobalVars
    import pdb
    
    savefilename = (QtGui.QFileDialog.getSaveFileName(ui,'Save Name/Directory', GlobalVars.Ch1DirPath, ''))
    GlobalVars.Ch1DirPath = QtCore.QFileInfo(savefilename[0]).path();
    GlobalVars.Ch1fileName = QtCore.QFileInfo(savefilename[0]).fileName();
    
    ui.Ch1FileNameLabel.setText("Filename: "+GlobalVars.Ch1fileName)
    ui.Ch1FileDirectoryLabel.setText("Directory: "+GlobalVars.Ch1DirPath)
    ui.Ch1checkBox.setEnabled(True);

    
def Ch2SaveDirPushButtonpushButtonClicked():
    import GlobalVars

    import os
    import GlobalVars
    
    savefilename = (QtGui.QFileDialog.getSaveFileName(ui,'Save Name/Directory', GlobalVars.Ch2DirPath, '.wav'))
    GlobalVars.Ch2DirPath = QtCore.QFileInfo(savefilename[0]).path();
    GlobalVars.Ch2fileName = QtCore.QFileInfo(savefilename[0]).fileName();

    
    ui.Ch2FileNameLabel.setText("Filename: "+GlobalVars.Ch2fileName)
    ui.Ch2FileDirectoryLabel.setText("Directory: "+GlobalVars.Ch2DirPath)
    ui.Ch2checkBox.setEnabled(True);

    
def Ch3SaveDirPushButtonpushButtonClicked():        
    import GlobalVars

    import os
    import GlobalVars
    
    savefilename = (QtGui.QFileDialog.getSaveFileName(ui,'Save Name/Directory', GlobalVars.Ch3DirPath, '.wav'))
    GlobalVars.Ch3DirPath = QtCore.QFileInfo(savefilename[0]).path();
    GlobalVars.Ch3fileName = QtCore.QFileInfo(savefilename[0]).fileName();

    ui.Ch3FileNameLabel.setText("Filename: "+GlobalVars.Ch3fileName)
    ui.Ch3FileDirectoryLabel.setText("Directory: "+GlobalVars.Ch3DirPath)
    ui.Ch3checkBox.setEnabled(True);

    
def Ch4SaveDirPushButtonpushButtonClicked():
    import os
    import GlobalVars
    
    savefilename = (QtGui.QFileDialog.getSaveFileName(ui,'Save Name/Directory', GlobalVars.Ch4DirPath, '.wav'))
    GlobalVars.Ch4DirPath = QtCore.QFileInfo(savefilename[0]).path();
    GlobalVars.Ch4fileName = QtCore.QFileInfo(savefilename[0]).fileName();

    ui.Ch4FileNameLabel.setText(GlobalVars.Ch4fileName)
    ui.Ch4FileDirectoryLabel.setText(GlobalVars.Ch4DirPath);
    ui.Ch4checkBox.setEnabled(True);
    
def loadConfig_ButtonPressed():
    import os
    import GlobalVars       
            
    loadfilename = (QtGui.QFileDialog.getOpenFileName(ui,'Open Config File', GlobalVars.Ch1DirPath,'*.TAFcfg'))  
    GlobalVars.loadConfig(loadfilename[0],ui)
    


def saveConfig_ButtonPressed():
    import GlobalVars
  
    savefilename = (QtGui.QFileDialog.getSaveFileName(ui,'Open Config File', GlobalVars.Ch1DirPath,'*.TAFcfg','*.TAFcfg'))  
    GlobalVars.saveConfig(savefilename[0],ui)

def updateSampleRate():
    import GlobalVars
    GlobalVars.SampleRate=int(ui.SampleRatecomboBox.currentText())
  
    
class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        from numpy import arange, array, zeros
        import GlobalVars;
        import pyaudio
        
        GlobalVars.buffertime=2
        GlobalVars.threshold1=500
        GlobalVars.threshold2=500
        GlobalVars.threshold3=500
        GlobalVars.threshold4=500
        GlobalVars.Ch1DirPath=''
        GlobalVars.Ch2DirPath=''
        GlobalVars.Ch3DirPath=''
        GlobalVars.Ch4DirPath=''
        GlobalVars.Ch1fileName=''
        GlobalVars.Ch2fileName=''
        GlobalVars.Ch3fileName=''
        GlobalVars.Ch4fileName=''        
        GlobalVars.inputdeviceindex=0
        GlobalVars.CHANNELS=4;
        GlobalVars.isRunning=False;
        GlobalVars.SampleRate=44100;

        self.ThresholdLineEdit1.setText(str(GlobalVars.threshold1))
        self.ThresholdLineEdit2.setText(str(GlobalVars.threshold2))
        self.ThresholdLineEdit3.setText(str(GlobalVars.threshold3))
        self.ThresholdLineEdit4.setText(str(GlobalVars.threshold4))        

        self.Ch1checkBox.setEnabled(False);
        self.Ch2checkBox.setEnabled(False);
        self.Ch3checkBox.setEnabled(False);
        self.Ch4checkBox.setEnabled(False);
        self.Ch1SaveDirPushButton.setEnabled(False);
        self.Ch2SaveDirPushButton.setEnabled(False);
        self.Ch3SaveDirPushButton.setEnabled(False);
        self.Ch4SaveDirPushButton.setEnabled(False);      
        self.actionLoad_Config.triggered.connect(loadConfig_ButtonPressed);
        self.actionSave_Config.triggered.connect(saveConfig_ButtonPressed);                

        self.RescanInputsPushButton.clicked.connect(RescanInputsButtonPushed)
        self.StopPushButton.clicked.connect(StopPushButton)
        self.StartPushButton.clicked.connect(StartPushButton)                                      
        self.BufferTimeSpinBox.valueChanged.connect(BufferTimeSpinBoxChanged) 

        self.InputSelectioncomboBox.currentIndexChanged.connect(InputSelectioncomboBoxChanged)        

        self.Ch1SaveDirPushButton.clicked.connect(Ch1SaveDirPushButtonpushButtonClicked)
        self.Ch2SaveDirPushButton.clicked.connect(Ch2SaveDirPushButtonpushButtonClicked)
        self.Ch3SaveDirPushButton.clicked.connect(Ch3SaveDirPushButtonpushButtonClicked)
        self.Ch4SaveDirPushButton.clicked.connect(Ch4SaveDirPushButtonpushButtonClicked)

        self.ThresholdLineEdit1.textChanged.connect(ThresholdLineEditChanged1);
        self.ThresholdLineEdit2.textChanged.connect(ThresholdLineEditChanged2);
        self.ThresholdLineEdit3.textChanged.connect(ThresholdLineEditChanged3);
        self.ThresholdLineEdit4.textChanged.connect(ThresholdLineEditChanged4);
        self.SampleRatecomboBox.currentIndexChanged.connect(updateSampleRate);
            
        
        #self.HighPassSpinBox.valueChanged.connect(GlobalVars.HighPass=newvalue);

            

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    RescanInputsButtonPushed()
    sys.exit(app.exec_())
    #window.show()
    sys.exit(app.exec_())


