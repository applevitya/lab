from ctypes import *
from  SDK import staticIO, device, dynamic_digital, dynamic_analog
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

iteration = 100

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

def pulse_to_structure(str_array: Array, dt: int):
    str_array = str_array.reshape((8,8))
    str_array = np.flip(str_array,axis=1)
    str_array = str_array.reshape((64,))

    print('Pulse to structure')
    dynamic_digital.led_matrix(hdwf,6,7,5,list(str_array))
    time.sleep(dt)
    dynamic_digital.led_matrix(hdwf,6,7,5,list(led_off))

    pass

################################################################################################################

known_indices = list(range(19, 25)) + list(range(27, 33)) + [34] + list(range(36, 41)) + list(range(43, 49)) + list(range(49, 50))
weights_array=np.empty(shape=(10000,len(known_indices)))

# stage1 - 10 sec
led = [0] * 64

led[known_indices[0] - 1:known_indices[3] - 1] = [1,1,1]
pulse_to_structure(np.array(led), 10)

# stage2 - 25 sec
led = [0] * 64

led[known_indices[3] - 1:known_indices[6] - 1] = [1,1,1]
pulse_to_structure(np.array(led), 25)


# stage3 - 35 sec
led = [0] * 64

led[known_indices[6] - 1:known_indices[9] - 1] = [1,1,1]
pulse_to_structure(np.array(led),35)

# stage4 - 45 sec
led = [0] * 64

led[known_indices[9] - 1:known_indices[12] - 1] = [1,1,1]
pulse_to_structure(np.array(led),45)



for i in range(0,len(weights_array)):
    time.sleep(1)
    for j,val in enumerate(known_indices):
        if val<33:
            weights_array[i][j] = measure(val)
        else:
            weights_array[i][j] = measure_2(val)



data = np.array(weights_array)
with open("results/motion.txt", "w") as file:
    np.savetxt(file, data)


device.close(hdwf)

