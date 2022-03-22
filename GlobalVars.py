
global isRunning
global numdevices
global devicenumber
global inputdeviceindex
global samplerateIDX
global CHANNELS

global Ch1DirPath
global Ch2DirPath
global Ch3DirPath
global Ch4DirPath
global Ch1fileName
global Ch2fileName
global Ch3fileName
global Ch4fileName

global threshold1
global threshold2
global threshold3
global threshold4



def loadConfig(loadfilename,ui):
    from configparser import SafeConfigParser
    import os
    import GlobalVars
    import serial
    from numpy import arange,array
   
    parser = SafeConfigParser()
    loadfilename=loadfilename.replace('/','\\')
   
    if not parser.read(str(loadfilename)): #.replace('/','\\')):
        raise(IOError, 'cannot load')
    
  
    GlobalVars.buffertime=int(parser.get('main','GlobalVars.buffertime'))
    GlobalVars.InputSelection=parser.get('main','GlobalVars.InputSelectionText');
        
    GlobalVars.Ch1DirPath=(parser.get('main','GlobalVars.Ch1DirPath'))
    GlobalVars.Ch2DirPath=(parser.get('main','GlobalVars.Ch2DirPath'))
    GlobalVars.Ch3DirPath=(parser.get('main','GlobalVars.Ch3DirPath'))
    GlobalVars.Ch4DirPath=(parser.get('main','GlobalVars.Ch4DirPath'))
    
    GlobalVars.Ch1fileName=(parser.get('main','GlobalVars.Ch1fileName'))
    GlobalVars.Ch2fileName=(parser.get('main','GlobalVars.Ch2fileName'))
    GlobalVars.Ch3fileName=(parser.get('main','GlobalVars.Ch3fileName'))
    GlobalVars.Ch4fileName=(parser.get('main','GlobalVars.Ch4fileName'))
     
    GlobalVars.threshold1=float(parser.get('main','GlobalVars.threshold1'))
    GlobalVars.threshold2=float(parser.get('main','GlobalVars.threshold2'))
    GlobalVars.threshold3=float(parser.get('main','GlobalVars.threshold3'))
    GlobalVars.threshold4=float(parser.get('main','GlobalVars.threshold4'))
    GlobalVars.SampleRate=int(parser.get('main','GlobalVars.SampleRate'))

    ui.Ch1FileNameLabel.setText(GlobalVars.Ch1fileName);
    ui.Ch1FileDirectoryLabel.setText(GlobalVars.Ch1DirPath);        
    ui.Ch2FileNameLabel.setText(GlobalVars.Ch2fileName)
    ui.Ch2FileDirectoryLabel.setText(GlobalVars.Ch2DirPath);        
    ui.Ch3FileNameLabel.setText(GlobalVars.Ch3fileName)
    ui.Ch3FileDirectoryLabel.setText(GlobalVars.Ch3DirPath);        
    ui.Ch4FileNameLabel.setText(GlobalVars.Ch4fileName)
    ui.Ch4FileDirectoryLabel.setText(GlobalVars.Ch4DirPath);
    ui.BufferTimeSpinBox.setValue(GlobalVars.buffertime)
    ui.ThresholdLineEdit1.setText(str(GlobalVars.threshold1))
    ui.ThresholdLineEdit2.setText(str(GlobalVars.threshold2))
    ui.ThresholdLineEdit3.setText(str(GlobalVars.threshold3))
    ui.ThresholdLineEdit4.setText(str(GlobalVars.threshold4))
    
    ui.SampleRatecomboBox.setCurrentText(str(GlobalVars.SampleRate)) 
    ui.InputSelectioncomboBox.setCurrentText(GlobalVars.InputSelection)
   
    
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
    

def saveConfig(savefilename,ui):
    from configparser import SafeConfigParser
    import os
    import GlobalVars
    from numpy import array    
    
    SaveFile= open((savefilename),'w')
    
    parser = SafeConfigParser()
    
    parser.add_section('main')

    
    parser.set('main','GlobalVars.buffertime',str(GlobalVars.buffertime))
    parser.set('main','GlobalVars.Ch1DirPath',str(GlobalVars.Ch1DirPath))
    parser.set('main','GlobalVars.Ch2DirPath',str(GlobalVars.Ch2DirPath))
    parser.set('main','GlobalVars.Ch3DirPath',str(GlobalVars.Ch3DirPath))
    parser.set('main','GlobalVars.Ch4DirPath',str(GlobalVars.Ch4DirPath))

    parser.set('main','GlobalVars.Ch1fileName',str(GlobalVars.Ch1fileName))
    parser.set('main','GlobalVars.Ch2fileName',str(GlobalVars.Ch2fileName))
    parser.set('main','GlobalVars.Ch3fileName',str(GlobalVars.Ch3fileName))
    parser.set('main','GlobalVars.Ch4fileName',str(GlobalVars.Ch4fileName))
    
    parser.set('main','GlobalVars.threshold1',str(GlobalVars.threshold1))
    parser.set('main','GlobalVars.threshold2',str(GlobalVars.threshold2))
    parser.set('main','GlobalVars.threshold3',str(GlobalVars.threshold3))
    parser.set('main','GlobalVars.threshold4',str(GlobalVars.threshold4))
    parser.set('main','GlobalVars.SampleRate',str(GlobalVars.SampleRate))
    parser.set('main','GlobalVars.InputSelectionText',ui.InputSelectioncomboBox.currentText()); 
        
    parser.write(SaveFile)    
    SaveFile.close()
