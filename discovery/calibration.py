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



############################################################################################################################################################
#calibration procedure



# known_indices = [22, 23, 24, 30]  # Заранее известные индексы
# initial_weights = []
# final_weights = []

# for index in known_indices:
#     value = measure(index)  # Получаем значение из функции measure
#     initial_weights.append(value)  # Добавляем значение в массив initial_weights

# print(initial_weights)

#led-stimulation
# dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_on)
# time.sleep(1000)
# dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off)


# for index in known_indices:
#     value = measure(index)  # Получаем значение из функции measure
#     final_weights.append(value)  # Добавляем значение в массив initial_weights

# print(final_weights)

# data=np.vstack((initial_weights,final_weights))
# # Запись массивов в файл
# with open("calibration.txt", "w") as file:
#     np.savetxt(file, data)



############################################################################################################################################################
#one impulse detection

known_indices = [24]
weights_array = []

start_time = time.time()

while len(weights_array)<20:
    value = measure(known_indices[0])
    current_time = time.time() - start_time
    weights_array.append((value, current_time))
    time.sleep(0.03)

#led-stimulation

while len(weights_array)<320:
    dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_on)
    time.sleep(1)
    dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off)

    value = measure(known_indices[0])
    current_time = time.time() - start_time
    weights_array.append((value, current_time))
    #time.sleep(0.00005)



while len(weights_array)<13000:
    value = measure(known_indices[0])
    current_time = time.time() - start_time  
    weights_array.append((value, current_time))
    time.sleep(1)


data = np.array(weights_array)
with open("results/calibration.txt", "w") as file:
    np.savetxt(file, data)




device.close(hdwf)