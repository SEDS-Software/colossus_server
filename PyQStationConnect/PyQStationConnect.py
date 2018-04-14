#-*- coding: utf-8 -*-

from ctypes import*
import ctypes
import numpy as np
# Load DLL into memory, take care to have the corresponding dll to the computer operating system
GINSDll = ctypes.cdll.LoadLibrary("C:/Users/Colossus_Laptop/colossus_server/giutility.dll")

#function prototypes
GINSDll._CD_eGateHighSpeedPort_Init.argtypes = [c_char_p,c_int,c_int,c_int,POINTER(c_int),POINTER(c_int)]
GINSDll._CD_eGateHighSpeedPort_SetBackTime.argtypes = [c_int, c_double]
GINSDll._CD_eGateHighSpeedPort_InitBuffer.argtypes=[c_int,c_int,c_int]
GINSDll._CD_eGateHighSpeedPort_DecodeFile_Select.argtypes = [POINTER(c_int), POINTER(c_int), c_char_p]
GINSDll._CD_eGateHighSpeedPort_GetDeviceInfo.argtypes = [c_int, c_int, c_int, POINTER(c_double), c_char_p]
GINSDll._CD_eGateHighSpeedPort_ReadBufferToDoubleArray.argtypes = [c_int, POINTER(c_double), c_int, c_int,
                                                                   POINTER(c_int), POINTER(c_int), POINTER(c_int)]
GINSDll._CD_eGateHighSpeedPort_Close.argtypes = [c_int, c_int]


class ConnectGIns():
    def __init__(self, buffer):
        """"  parameters for Init connection """
        self.controllerIP=0#controllerIP.encode('UTF-8')
        self.timeout=5
        self.HSP_BUFFER=2#  1 for online; 2 for buffered values
        self.sampleRate=100
        # parameters for file decoding
        self.FilePath=0# = FilePath.encode('UTF-8')
        self.FileDecodeComplete=False
        #general used parameters
        self.HCLIENT=c_int(-1)
        self.HCONNECTION=c_int(-1)
        #parameters for Init buffer
        self.bufferindex=buffer
        self.autoRun=0
        #parameters to empty the circular buffer
        self.backtime=0
        #parameters to read information from devices
        self.location=10
        self.Adress=11
        self.SampleRate=16
        self.SerialNumber=15
        self.ChannelCount=18
        self.Channel_InfoName=0
        self.Channel_Unit=1
        self.info=c_double(0)
        self.ret=0
        self.char=ctypes.create_string_buffer(30)
        #parameters to read buffer
        
        
    def init_connection(self,controllerIP):
        self.controllerIP=controllerIP.encode('UTF-8')
        """Initialisation of the connection to a controller"""
        ret=GINSDll._CD_eGateHighSpeedPort_Init(self.controllerIP,self.timeout,self.HSP_BUFFER,self.sampleRate,byref(self.HCLIENT),byref(self.HCONNECTION))
        if(ret!=0):
            print("Init Connection Failed - ret:",ret)
            return False
        #Init buffer (this is mainly to select a certain buffer by index)
        ret=GINSDll._CD_eGateHighSpeedPort_InitBuffer(self.HCONNECTION.value,self.bufferindex,self.autoRun)
        if(ret!=0):
            print("Init Buffer Failed - ret:",ret)
            return False
        #empty the circular buffer to get only actual data
        ret=GINSDll._CD_eGateHighSpeedPort_SetBackTime(self.HCONNECTION.value,self.backtime)
        if(ret!=0):
            print("SetBackTime Failed - ret:",ret)
            return False
        print("Connection initialized. IP: ", controllerIP)
        return True

    def init_file(self,FilePath):
        """Initialisation of the dat-file"""
        self.FilePath= FilePath.encode('UTF-8')
        ret=GINSDll._CD_eGateHighSpeedPort_DecodeFile_Select(byref(self.HCLIENT),byref(self.HCONNECTION),self.FilePath)
        if ret==0:
            print("File Load OK!", self.FilePath.decode('UTF-8'))
            return True
        else:
            print("Error Loading File ", self.FilePath.decode('UTF-8'))
            return False

    def read_serial_number(self):
        """Read the serial number of the connected device"""
        ret=GINSDll._CD_eGateHighSpeedPort_GetDeviceInfo(self.HCONNECTION.value,self.SerialNumber,0,self.info,None)
        if(ret==0):
            print("controller serial number", self.info.value)
            return self.info.value
        else:
            print("error reading serial number!")
            return 0
                
    def read_sample_rate(self):
        """Read a buffer sampling rate"""
        ret=GINSDll._CD_eGateHighSpeedPort_GetDeviceInfo(self.HCONNECTION.value,self.SampleRate,0,self.info,None)
        if(ret==0):
            print("controller sample rate", self.info.value)
            return self.info.value
        else:
            print("Error reading sample rate!")
            return 0
        
    def read_channel_count(self):
        """Count the number of channels connected to a controller"""
        ret=GINSDll._CD_eGateHighSpeedPort_GetDeviceInfo(self.HCONNECTION.value,self.ChannelCount,0,self.info,None)
        if(ret==0):
            print("controller channel count", self.info.value)
            return self.info.value
        else:
            print("Error reading channel count!")
            return ""
    
    def read_controller_name(self):
        """Read a controller name"""
        #p=ctypes.create_string_buffer(30)#this function works for python 3.6, for lower version the name of functions to create mutable character buffer is different
        ret=GINSDll._CD_eGateHighSpeedPort_GetDeviceInfo(self.HCONNECTION.value,self.location,0,None,self.char)
        if(ret==0):
            print("controller name", self.char.value.decode('UTF-8'))
            return self.char.value.decode('UTF-8')
        else:
            print("Error reading controller name!")
            return ""
        
    def read_controller_address(self):
        """Read the adress of a connected controller"""
        ret=GINSDll._CD_eGateHighSpeedPort_GetDeviceInfo(self.HCONNECTION.value,self.Adress,0,None,self.char)
        if(ret==0):
            print("controller adress", self.char.value.decode('UTF-8'))
            return self.char.value.decode('UTF-8')
        else:
            print("Error reading controller address")
            return ""
        
    def read_channel_names(self):
        """Read the channel name and corresponding index"""
        i=0
        GINSDll._CD_eGateHighSpeedPort_GetDeviceInfo(self.HCONNECTION.value,self.ChannelCount,0,self.info,None)
        ChannelNb=self.info.value
        while i<ChannelNb:
            GINSDll._CD_eGateHighSpeedPort_GetDeviceInfo(self.HCONNECTION.value,self.Channel_InfoName,i,None,self.char)
            print("Controller index:",i," channel name:", self.char.value.decode('UTF-8'))
            i+=1
            
    def read_index_name(self,IndexNb):
        """Read the channel name corresponding to an index"""
        ret=GINSDll._CD_eGateHighSpeedPort_GetDeviceInfo(self.HCONNECTION.value,self.Channel_InfoName,IndexNb,None,self.char)
        if(ret==0):
            return(self.char.value.decode('UTF-8'))
        else:
            print("Error reading channel name, index",IndexNb)
            return ""
    
    #def read_buffer_frame(self):
    #    GINSDll._CD_eGateHighSpeedPort_GetBufferFrames.argtypes=[c_int,c_int]
    #    GINSDll._CD_eGateHighSpeedPort_GetBufferFrames(self.HCONNECTION.value,self.HCLIENT.value)
    #    print("buffer frame number:",)
        
    
    def yield_buffer(self,NbFrames=int(10000),fillArray=0):

        GINSDll._CD_eGateHighSpeedPort_GetDeviceInfo(self.HCONNECTION.value,self.ChannelCount,0,self.info,None)
        ChannelNb=int(self.info.value)
        valuesPtr=(c_double*(NbFrames*ChannelNb))()
        ReceivedFrames=c_int(0)#pointer
        ReceivedChannels=c_int(0)#pointer
        ReceivedComplete=c_int(0)#pointer
        ret=0
        while(ret==0):
            ret=GINSDll._CD_eGateHighSpeedPort_ReadBufferToDoubleArray(self.HCONNECTION.value,valuesPtr,(NbFrames*ChannelNb),fillArray,ReceivedFrames,ReceivedChannels,ReceivedComplete)
            chcnt=ReceivedChannels.value
            BUF=valuesPtr[0:chcnt*ReceivedFrames.value]
            buffer=np.reshape(BUF,(ReceivedFrames.value,chcnt))
            yield buffer


    def close_connection(self):
        GINSDll._CD_eGateHighSpeedPort_Close(self.HCONNECTION.value,self.HCLIENT.value)



