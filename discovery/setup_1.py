from ctypes import *
from SDK import staticIO, device, dynamic_digital, dynamic_analog
import sys
import numpy as np
import pandas as pd
import time


from matplotlib.figure import Figure


##### инициализирование####################################################################################################################################
hdwf = c_int()
hdwf = device.open()


led_off = [0 for i in range(64)]
led_on = [1 for i in range(64)]
dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off) # выключаем светодиоды

iteration = 50


def measure(index): # сюда подаются именно номера структур
    struct_index = [0 for i in range(64)]
    struct_index[index-1] = 1
    dynamic_analog.struct_measure(hdwf, 10, 9, 8, struct_index) # struct_measure(device_handle,shift,clock,data,matrix)
    values = []
    for i in range(iteration):
        values.append(dynamic_analog.measure(hdwf, 1))
    return sum(values) / len(values)


def measure_2(index): # сюда подаются именно номера структур
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
        time.sleep(3)
        dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off)

        for i, val in enumerate(arr):
            if val != 0:
                if i<32:
                    value[i] = measure(i+1)
                else:
                    value[i] = measure_2(i+1)
    return value

def pulse_to_structure(str_array):
    str_array = str_array.reshape((8,8))
    str_array = np.flip(str_array,axis=1)
    str_array = str_array.reshape((64,))

    dynamic_digital.led_matrix(hdwf,6,7,5,list(str_array))
    time.sleep(10)
    dynamic_digital.led_matrix(hdwf,6,7,5,list(led_off))

    pass






####################################################################################################################################

## зададим картинку

pic = np.loadtxt('experiment/start.txt')

pic = pic*2.2980424272707376/255
pic = pic.reshape(-1)

indexes = list(range(19, 25)) + list(range(27, 33)) + [34] + list(range(36, 41)) + list(range(43, 49)) + list(range(49, 50))
weights = [0] * 64

for i, index in enumerate(indexes):
    weights[index-1] = pic[i]


weight_setting(weights) # задали картинку 

####### Эксперимент

df= pd.read_csv('experiment/event.csv') # файл с events
df.drop(columns=['Unnamed: 0'])

for i in range(df.shape[0]):
    for j, index in enumerate(indexes):
        leds_array = [0]*64
        leds_array[index-1] = df.loc[i].to_numpy()[j]
        pulse_to_structure(leds_array)

        