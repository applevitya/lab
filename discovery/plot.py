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

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")


##### инициализирование############################################
hdwf = c_int()
hdwf = device.open()


led_off = [0 for i in range(64)]
led_on = [1 for i in range(64)]
dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off) # выключаем светодиоды

struct_index = [0 for i in range(64)]
struct_index[20] = 1
dynamic_analog.struct_measure(hdwf, 10, 9, 8, struct_index) # struct_measure(device_handle,shift,clock,data,matrix)


####################################################################

def measure(index):
    struct_index = [0 for i in range(64)]
    struct_index[index-1] = 1
    dynamic_analog.struct_measure(hdwf, 10, 9, 8, struct_index) # struct_measure(device_handle,shift,clock,data,matrix)
    values = []
    for i in range(60):
        values.append(dynamic_analog.measure(hdwf, 1))
    return sum(values) / len(values)

def some_function():
    position = np.zeros(64)
    position[2] = 1
    dynamic_digital.led_matrix(hdwf, 6, 7, 5, list(position))
    time.sleep(5)
    dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off)
    print("Выполняется функция, не связанная с графиком")

def close():
    device.close(hdwf)
    print("Закрытие программы")

def update_graphs():
    global x, y1, y2,  y3 ,y4, counter

    if not stop_graph:
        x.append(counter)
        y1.append(measure(21))
        y2.append(measure(22))
        y3.append(measure(28))
        y4.append(measure(29))
        counter += 1

        lines1.set_data(x, y1)
        lines2.set_data(x, y2)
        lines3.set_data(x, y3)
        lines4.set_data(x, y4)

        ax1.relim()
        ax1.autoscale_view()
        ax2.relim()
        ax2.autoscale_view()
        ax3.relim()
        ax3.autoscale_view()
        ax4.relim()
        ax4.autoscale_view()

        canvas.draw()

        root.after(10, update_graphs)

def stop():
    global stop_graph
    stop_graph = True
    dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off)
    close()
    root.quit()


###########################################

def alignment():
    print('aligment start')
    position = np.zeros(64)
    position[20] = position[21] = 1
    # Создаем массив значений
    value = np.zeros(64)
    values = [measure(i + 1) for i in range(len(position)) if position[i] == 1]
    value[position == 1] = values
    print(value[20])

    # Находим максимальное значение и индекс элемента с максимальным значением
    max_value = np.max(values)
    max_index = np.argmax(values)

    # Первоначально все элементы не меняем
    array = np.zeros(64)

    # Устанавливаем 0 на месте элемента с максимальным значением, чтобы его не менять
    array[position == 1][max_index] = 0

    # Пока все значения не сравняются с точностью +-0.015 для самого большого изначального числа
    while np.any(np.abs(value[position == 1] - max_value) > 0.25):
        # Устанавливаем 1 на месте элементов, которые необходимо изменить
        array[position == 1] = np.where(np.abs(value[position == 1] - max_value) > 0.10, 1, array[position == 1])
        print(array)

        # Запускаем функцию изменения параметров элементов
        dynamic_digital.led_matrix(hdwf, 6, 7, 5, array)

        # Ждем некоторое время, чтобы изменения успели примениться
        time.sleep(1)
        dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off)

        # Считываем новые значения и обновляем массив значений
        values = [measure(i + 1) for i in range(len(position)) if position[i] == 1]
        value[position == 1] = values

    return value

############################################

root = tk.Tk()
root.title("Tkinter и Matplotlib")
root.geometry("1000x600")

frame_buttons = ttk.Frame(root)
frame_buttons.pack(side=tk.TOP, pady=20)

btn_some_function = ttk.Button(frame_buttons, text="Выполнить функцию", command=some_function)
btn_some_function.pack(side=tk.LEFT, padx=10)

btn_close = ttk.Button(frame_buttons, text="Закрыть", command=stop)
btn_close.pack(side=tk.LEFT, padx=10)

fig, (ax1, ax2,ax3,ax4) = plt.subplots(nrows=4, ncols=1, figsize=(7, 5))
lines1, = ax1.plot([], [], lw=2)
lines2, = ax2.plot([], [], lw=2)
lines3, = ax3.plot([], [], lw=2)
lines4, = ax4.plot([], [], lw=2)
ax1.set_title("21 место")
ax2.set_title(" 22 место")
ax3.set_title("23 место")
ax4.set_title(" 24 место")


canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

x, y1, y2, y3,y4 = [], [], [],[],[]
counter = 0
stop_graph = False

root.after(10, update_graphs)
root.mainloop()
