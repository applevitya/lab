""" DEVICE CONTROL FUNCTIONS: open, check_error, close """

import sys
import ctypes
from SDK import staticIO

"""-----------------------------------------------------------------------"""

if sys.platform.startswith("win"):
    dwf = ctypes.cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")

hzSys = ctypes.c_double()
"""-----------------------------------------------------------------------"""




def rectangular_pulses(device_handle,channel,frequency): #freq in Hz
    frequency = frequency/10
    dwf.FDwfDigitalOutInternalClockInfo(device_handle, ctypes.byref(hzSys))
    
    dwf.FDwfDigitalOutEnableSet(device_handle, ctypes.c_int(channel), ctypes.c_int(1)) #pulse on IO pin
    dwf.FDwfDigitalOutDividerSet(device_handle, ctypes.c_int(channel), ctypes.c_int(int(hzSys.value/2e1/frequency)))
    dwf.FDwfDigitalOutCounterSet(device_handle, ctypes.c_int(channel), ctypes.c_int(1), ctypes.c_int(1)) ## 1 tick low, 1 tick high
    dwf.FDwfDigitalOutCounterInitSet(device_handle, ctypes.c_int(channel), ctypes.c_int(1), ctypes.c_int(0)) #начинать с high on start
    dwf.FDwfDigitalOutConfigure(device_handle, ctypes.c_int(1))
    return
"""-----------------------------------------------------------------------"""


def pulse(device_handle,channel,duration): #duration in s
    dwf.FDwfDigitalOutRunSet(device_handle, ctypes.c_double(duration)) # second run
    dwf.FDwfDigitalOutRepeatSet(device_handle, ctypes.c_int(1)) # once
    dwf.FDwfDigitalOutIdleSet(device_handle, ctypes.c_int(channel), ctypes.c_int(1)) # 1=DwfDigitalOutIdleLow, low when not running
    dwf.FDwfDigitalOutCounterInitSet(device_handle, ctypes.c_int(channel), ctypes.c_int(1), ctypes.c_int(0)) # initialize high on start
    dwf.FDwfDigitalOutCounterSet(device_handle, ctypes.c_int(channel), ctypes.c_int(0), ctypes.c_int(0)) # low/high count zero, no toggle during run
    dwf.FDwfDigitalOutEnableSet(device_handle, ctypes.c_int(channel), ctypes.c_int(1))
    dwf.FDwfDigitalOutConfigure(device_handle, ctypes.c_int(1))
    return




"""-----------------------------------------------------------------------"""



def led_matrix(device_handle,shift,clock,data,matrix):
    staticIO.turn_off_channel(device_handle,shift)
    
    for i in range(len(matrix)):
        if bool(matrix[i]) == True:
            staticIO.turn_on_channel(device_handle,data)
            
            staticIO.turn_on_channel(device_handle,clock)
            staticIO.turn_off_channel(device_handle,clock)
            staticIO.turn_off_channel(device_handle,data)
        else:
            staticIO.turn_on_channel(device_handle,data)
            
            staticIO.turn_on_channel(device_handle,clock)
            staticIO.turn_off_channel(device_handle,clock)
            staticIO.turn_off_channel(device_handle,data)
            
    staticIO.turn_on_channel(device_handle,shift)
    return
    

    
