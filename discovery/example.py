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

t_start = time.process_time()



data1 = [1 for i in range(64)]
data2 = [0 for i in range(64)]

datanew=[0 for i in range(64)]
for i in range(64):
    if i%2==0: datanew[i] = 1
    else: datanew[i] = 0

dynamic_digital.led_matrix(hdwf,1,2,0,data2)
#dynamic_digital.pulse(hdwf,5,0.002)

for j in range(400):
	dynamic_digital.led_matrix(hdwf,1,2,0,data2)
	time.sleep(0.00005)
	dynamic_digital.led_matrix(hdwf,1,2,0,data2)
	time.sleep(0.00005)


dynamic_analog.measure(hdwf,1)

print(time.process_time() - t_start)

dwf.FDwfDigitalOutReset(hdwf)
device.close(hdwf)




