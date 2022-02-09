"""
   DWF Python Example
   Requires:                       
       Python 2.7, 3
"""

import ctypes
from  SDK import staticIO, device, dynamic_digital
import sys
import time

if sys.platform.startswith("win"):
    dwf = ctypes.cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")


    
hdwf = ctypes.c_int()
hdwf = device.open()


dynamic_digital.digital_rectangular_pulse(hdwf,1,100)

time.sleep(30)


device.close(hdwf)




