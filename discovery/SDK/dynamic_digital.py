""" DEVICE CONTROL FUNCTIONS: open, check_error, close """

import sys
import ctypes


"""-----------------------------------------------------------------------"""

if sys.platform.startswith("win"):
    dwf = ctypes.cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")

hzSys = ctypes.c_double()

def digital_rectangular_pulse(device_handle,channel,frequency): #freq in Hz
    dwf.FDwfDigitalOutInternalClockInfo(device_handle, ctypes.byref(hzSys))
    
    dwf.FDwfDigitalOutEnableSet(device_handle, ctypes.c_int(channel), ctypes.c_int(1)) #pulse on IO pin
    dwf.FDwfDigitalOutDividerSet(device_handle, ctypes.c_int(channel), ctypes.c_int(int(hzSys.value/2e1/frequency)))
    dwf.FDwfDigitalOutCounterSet(device_handle, ctypes.c_int(channel), ctypes.c_int(1), ctypes.c_int(1)) ## 1 tick low, 1 tick high
    dwf.FDwfDigitalOutConfigure(device_handle, ctypes.c_int(1))
    return

def led_matrix(device_handle,shift,clock,data,matrix):
    staticIO.turn_off_channel(device_handle,shift)
    
