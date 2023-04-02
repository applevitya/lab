"""
   DWF Python Example
   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
from  SDK import staticIO, device, dynamic_digital, dynamic_analog
import sys
import time
import asyncio
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")


    
hdwf = c_int()
hdwf = device.open()



t_start = time.process_time()


###############################################


led_off = [0 for i in range(64)]
led_on = [1 for i in range(64)]
position = [0 for i in range(64)]
position[0] =1



dynamic_digital.led_matrix(hdwf,6,7,5,led_off)
time.sleep(0.02)

for i in range(10):
    dynamic_digital.led_matrix(hdwf,6,7,5,led_off)
    time.sleep(0.04)
    dynamic_digital.led_matrix(hdwf,6,7,5,position)
    time.sleep(0.04)

dynamic_digital.led_matrix(hdwf,6,7,5,position)

device.close(hdwf)













