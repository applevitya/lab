"""
   DWF Python Example
   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
from  SDK import staticIO, device, dynamic_digital
import sys
import time
import asyncio

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")


    
hdwf = c_int()
hdwf = device.open()

# channel 0 - data
# channel 1 - shift
# channel 2 - clock



data1 = [1 for i in range(64)]
data2 = [0 for i in range(64)]


dynamic_digital.led_matrix(hdwf,1,2,0,data1)


dwf.FDwfDigitalOutReset(hdwf)

device.close(hdwf)




