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

# channel 0 - clock
# channel 1 - shift
# channel 2 - data
# channel 3 - reset



hdwf = c_int()

version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))


print("Opening first device")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == 0:
    print("failed to open device")
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(str(szerr.value))
    quit()


data_for_led = [1 for i in range(63)]
dynamic_digital.led_matrix(hdwf,0,1,2)







dwf.FDwfDigitalOutReset(hdwf)

device.close(hdwf)




