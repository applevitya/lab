from ctypes import *
from  SDK import staticIO, device, dynamic_digital, dynamic_analog
import sys
import numpy as np
import tkinter as tk
from tkinter import ttk
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.figure import Figure


##### инициализирование####################################################################################################################################
hdwf = c_int()
hdwf = device.open()


led_off = [0 for i in range(64)]
led_on = [1 for i in range(64)]
dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off) # выключаем светодиоды

############################################################################################################################################################
#calibration procedure



known_indices = [1, 5, 10, 15]  # Заранее известные индексы
initial_weights = []
final_weights = []

for index in known_indices:
    value = measure(index)  # Получаем значение из функции measure
    initial_weights.append(value)  # Добавляем значение в массив initial_weights

print(initial_weights)  

#led-stimulation
dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_on)
time.sleep(1)
dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off)


for index in known_indices:
    value = measure(index)  # Получаем значение из функции measure
    final_weights.append(value)  # Добавляем значение в массив initial_weights

print(final_weights)

# Запись массивов в файл
with open("calibration.txt", "w") as file:
    np.savetxt(file, data)
