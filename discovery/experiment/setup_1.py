from ctypes import *
from  ..SDK import staticIO, device, dynamic_digital, dynamic_analog
import sys
import numpy as np

import time


from matplotlib.figure import Figure


##### инициализирование####################################################################################################################################
hdwf = c_int()
hdwf = device.open()


led_off = [0 for i in range(64)]
led_on = [1 for i in range(64)]
dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off) # выключаем светодиоды

iteration = 500

def measure(index):
    struct_index = [0 for i in range(64)]
    struct_index[index-1] = 1
    dynamic_analog.struct_measure(hdwf, 10, 9, 8, struct_index) # struct_measure(device_handle,shift,clock,data,matrix)
    values = []
    for i in range(iteration):
        values.append(dynamic_analog.measure(hdwf, 1))
    return sum(values) / len(values)

def measure_2(index):
    struct_index = [0 for i in range(64)]
    struct_index[index-1] = 1
    dynamic_analog.struct_measure(hdwf, 10, 9, 8, struct_index) # struct_measure(device_handle,shift,clock,data,matrix)
    values = []
    for i in range(iteration):
        values.append(dynamic_analog.measure(hdwf, 2))
    return sum(values) / len(values)

def weight_setting(arr):
    value = []
    for i, val in enumerate(arr):
        if val != 0:
            if i<32:
                value.append(measure(i+1))
            else:
                value.append(measure_2(i+1))
        else:
            value.append(0)
            
    while any(abs(a - b) > 0.02 for a, b in zip(arr, value)):
        led = np.array([int((a - b) > 0.02) for a, b in zip(arr, value)])
        led = led.reshape((8,8))
        led = np.flip(led,axis=1)
        led = led.reshape((64,))
        print(led)
        dynamic_digital.led_matrix(hdwf, 6, 7, 5, list(led))
        time.sleep(0.1)
        dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off)

        for i, val in enumerate(arr):
            if val != 0:
                if i<32:
                    value[i] = measure(i+1)
                else:
                    value[i] = measure_2(i+1)
    return value

####################################################################################################################################

## зададим картинку

pic = np.loadtxt('start.txt')
pic = pic*2.2987315479909154/255
pic = pic.reshape(-1)

indexes = list(range(19, 25)) + list(range(27, 33)) + [34] + list(range(36, 41)) + list(range(43, 49)) + list(range(49, 50))
weights = [0] * 64

for i, index in enumerate(indexes):
    weights[index-1] = pic[i]


weight_setting(weights) # задали картинку 

####### 


