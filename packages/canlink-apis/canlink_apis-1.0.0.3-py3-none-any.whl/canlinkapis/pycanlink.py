#Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006 Python Software Foundation; All Rights Reserved


import time, os, mmap
from os.path import *
from win32com.client import *
from win32com.client.connect import *

def PumpEvents():
    pythoncom.PumpWaitingMessages()
    time.sleep(.1)

def ExecuteEvents(state):
    while not state:         
        PumpEvents()

class CANlinkCOM(object):
    Started = False
    Stopped = False
    
    def __init__(self):
        CANlink = win32com.client.Dispatch("HanilProtech.CANlink")
        self.App = CANlink
        self.WaitForExecute = lambda: ExecuteEvents(lambda: CANlinkCOM.Started)
        self.WaitForStop  = lambda: ExecuteEvents(lambda: CANlinkCOM.Stopped)
        
    # Load hcf file.
    def LoadConfigFile(self,CfgPath):
        self.App.LoadConfigFile(CfgPath)
        time.sleep(1)
    
    # Execute Environment Modules.
    # Only the module with the check box displayed in the 'Test Setup Dialog' operates.
    def RunTestModule(self):
        self.App.RunTestModules()
        #PumpEvents()

    #CANlink Execute.
    def Start(self):
        self.Started = True
        self.Stopped = False
        self.App.Start()
        self.WaitForExecute()

    #CANlink Stop.
    def Stop(self):
        self.Started = False
        self.Stopped = True
        self.App.Stop()
        self.WaitForStop()
    
    #Export the Environment as xmlfile.
    def ExportTestModule(self,strPath):
        self.App.ExportTestSetupFile(strPath)
        time.sleep(1)

    #Import the Environment of xmlfile.
    def ImportTestModule(self,strPath):
        self.App.OpenTestEnvironment(strPath)
        time.sleep(1)
    
    # Wait for TestSetUpModule to be done    
    def WaitForTestSetupDone(self):
        while True:
            time.sleep(1)
            memory = mmap.mmap(-1,1,"Local\\testsetup", access=mmap.ACCESS_READ )
            buf = memory.readline()
            if buf == bytes(b'T'): #return 'T' when done 
                memory.close()
                return True
            memory.close()

# Returns a file list of '*.hcf' existing in the 'path' path.
def RunTestConfigFiles(path):
    file_list = os.listdir(path)
    new_file_list =[]
    
    for i in range(len(file_list)):
        fn = file_list[i]
        if os.path.splitext(fn)[1] == '.hcf':
            new_file_list.append(file_list[i])
    
    return new_file_list

# Returns path and file name combined.
def SettingPath(path,cfgName):
    dirret = isdir(path)
    if(dirret) :
        cfg = os.path.join(path,cfgName)
        cfg = os.path.abspath(cfg)
    else :
        print('Please enter correctly path')
        return None
    return cfg