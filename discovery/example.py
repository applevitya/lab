"""
   DWF Python Example
   Requires:                       
       Python 2.7, 3
"""

import ctypes
from  SDK import staticIO, device, dynamic_digital
import sys
import time

import asyncio

if sys.platform.startswith("win"):
    dwf = ctypes.cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")


    
hdwf = ctypes.c_int()
hdwf = device.open()

# channel 0 - clock
# channel 1 - shift
# channel 2 - data
# channel 3 - reset










dwf.FDwfDigitalOutReset(hdwf)

device.close(hdwf)




