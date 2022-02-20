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

# channel 0 - shift
# channel 1 - clock
# channel 2 - data
# channel 3 - reset

def led_matrix(matrix_array):
    staticIO.turn_off_channel(hdwf,1)
    
    for i in range(len(matrix_array)):
        staticIO.turn_on_channel(hdwf,2)
        
        staticIO.turn_off_channel(hdwf,0)
        staticIO.turn_on_channel(hdwf,0)
        
    staticIO.turn_on_channel(hdwf,1)
    
    return
 

led_matrix([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
time.sleep(1)

device.close(hdwf)




