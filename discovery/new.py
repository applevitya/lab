from ctypes import *
from  SDK import staticIO, device, dynamic_digital, dynamic_analog
import sys
import time
import asyncio
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output
from collections import defaultdict


if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")


    
hdwf = c_int()
hdwf = device.open()


# led matrix

#channel 0 - data
#channel 1 - shift (сдвиг)
#channel 2 - clock (тактовые импульсы после каждого сигнала)

led_off = [0 for i in range(64)]
led_on = [1 for i in range(64)]


dynamic_digital.led_matrix(hdwf,1,2,0,led_off)



# structure measure

#channel 5 - data
#channel 6 - shift (сдвиг)
#channel 7 - clock (тактовые импульсы после каждого сигнала)

struct_index = [0 for i in range(64)]
struct_index[7] = 1
print(len(struct_index))
dynamic_analog.struct_measure(hdwf,4,5,6,struct_index) # struct_measure(device_handle,shift,clock,data,matrix)

print(dynamic_analog.measure(hdwf,1))


# вывод графика



for i in range(10):
	dynamic_digital.led_matrix(hdwf,1,2,0,led_off)
	time.sleep(0.5)
	print(dynamic_analog.measure(hdwf,1))

	
	
	dynamic_digital.led_matrix(hdwf,1,2,0,led_on)
	time.sleep(0.5)
	print(dynamic_analog.measure(hdwf,1))

	
	time.sleep(0.00001)

dynamic_digital.led_matrix(hdwf,1,2,0,led_off)


dwf.FDwfDigitalOutReset(hdwf)
device.close(hdwf)



