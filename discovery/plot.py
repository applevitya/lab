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


##### инициализирование####################################################################################################################################
hdwf = c_int()
hdwf = device.open()


led_off = [0 for i in range(64)]
led_on = [1 for i in range(64)]
dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off) # выключаем светодиоды

############################################################################################################################################################






def measure(index):
    struct_index = [0 for i in range(64)]
    struct_index[index-1] = 1
    dynamic_analog.struct_measure(hdwf, 10, 9, 8, struct_index) # struct_measure(device_handle,shift,clock,data,matrix)
    values = []
    for i in range(200):
        values.append(dynamic_analog.measure(hdwf, 1))
    return sum(values) / len(values)

def measure_2(index):
    struct_index = [0 for i in range(64)]
    struct_index[index-1] = 1
    dynamic_analog.struct_measure(hdwf, 10, 9, 8, struct_index) # struct_measure(device_handle,shift,clock,data,matrix)
    values = []
    for i in range(100):
        values.append(dynamic_analog.measure(hdwf, 2))
    return sum(values) / len(values)

def all_led(t):
    dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_on)
    time.sleep(t)
    dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off)
    print("Выполняется функция, включения всех светодиодов")

def close():
    device.close(hdwf)
    print("Закрытие программы")

def update_graphs():
    global x, y1,y2,y3,y4,y5,y6,y7,y8, counter

    if not stop_graph:
        x.append(counter)
        y1.append(measure(21))
        y2.append(measure(22))
        y3.append(measure(23))
        y4.append(measure(24))
        y5.append(measure(29))
        y6.append(measure(30))
        y7.append(measure(31))
        y8.append(measure(32))

        counter += 1

        lines1.set_data(x, y1)
        lines2.set_data(x, y2)
        lines3.set_data(x, y3)
        lines4.set_data(x, y4)
        lines5.set_data(x, y5)
        lines6.set_data(x, y6)
        lines7.set_data(x, y7)
        lines8.set_data(x, y8)


        ax1.relim()
        ax1.autoscale_view()
        ax2.relim()
        ax2.autoscale_view()
        ax3.relim()
        ax3.autoscale_view()
        ax4.relim()
        ax4.autoscale_view()
        ax5.relim()
        ax5.autoscale_view()
        ax6.relim()
        ax6.autoscale_view()
        ax7.relim()
        ax7.autoscale_view()
        ax8.relim()
        ax8.autoscale_view()

        canvas.draw()

        root.after(5, update_graphs)

def stop():
    global stop_graph
    stop_graph = True
    dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off)
    close()
    root.quit()


###################################################################################################################################

def alignment(position):
    print('aligment start')
    position = np.array(position)
    # Создаем массив значений
    value = np.zeros(64)
    values = [measure(i + 1) for i in range(len(position)) if position[i] == 1]
    value[position == 1] = values
    print(value[20])

    # Находим максимальное значение и индекс элемента с максимальным значением
    max_value = np.max(values)
    max_index = np.argmax(values)





    # Пока все значения не сравняются с точностью +-0.015 для самого большого изначального числа
    while np.any(np.abs(value[position == 1] - max_value) > 0.03):
        array = np.zeros(64)
        array[position == 1][max_index] = 0
        # Устанавливаем 1 на месте элементов, которые необходимо изменить
        array[position == 1] = np.where((-value[position == 1] + max_value) > 0.03, 1, array[position == 1])
        array = array.reshape((8,8))
        array = np.flip(array,axis=1)
        array = array.reshape((64,))

        print(array)

        # Запускаем функцию изменения параметров элементов
        dynamic_digital.led_matrix(hdwf, 6, 7, 5, list(array))

        # Ждем некоторое время, чтобы изменения успели примениться
        time.sleep(0.005)
        dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off)

        # Считываем новые значения и обновляем массив значений
        values = [measure(i + 1) for i in range(len(position)) if position[i] == 1]
        value[position == 1] = values

    return 0





def weight_setting(arr):
    value = []
    for i, val in enumerate(arr):
        if val != 0:
            value.append(measure(i+1))
        else:
            value.append(0)
            
    while any(abs(a - b) > 0.02 for a, b in zip(arr, value)):
        led = np.array([int((a - b) > 0.02) for a, b in zip(arr, value)])
        led = led.reshape((8,8))
        led = np.flip(led,axis=1)
        led = led.reshape((64,))
        dynamic_digital.led_matrix(hdwf, 6, 7, 5, list(led))
        time.sleep(0.005)
        dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off)
        update_graphs()

        for i, val in enumerate(arr):
            if val != 0:
                value[i] = measure(i+1)
    return value



weights = [0] * 64
weights[20:24] = [0.2] * 4
weights[28:32] = [0.2] * 4
####################################################################################################################################




root = tk.Tk()
root.title("Tkinter и Matplotlib")
root.geometry("1300x800")

frame_buttons = ttk.Frame(root)
frame_buttons.pack(side=tk.TOP, pady=20)

btn_some_function = ttk.Button(frame_buttons, text="Включаем все светодиоды", command=lambda: weight_setting(weights))
btn_some_function.pack(side=tk.LEFT, padx=10)

btn_close = ttk.Button(frame_buttons, text="Закрыть", command=stop)
btn_close.pack(side=tk.LEFT, padx=10)

fig, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8)) = plt.subplots(nrows=2, ncols=4, figsize=(12, 9))
lines1, = ax1.plot([], [], lw=2)
lines2, = ax2.plot([], [], lw=2)
lines3, = ax3.plot([], [], lw=2)
lines4, = ax4.plot([], [], lw=2)
lines5, = ax5.plot([], [], lw=2)
lines6, = ax6.plot([], [], lw=2)
lines7, = ax7.plot([], [], lw=2)
lines8, = ax8.plot([], [], lw=2)

ax1.set_title("21 str")
ax2.set_title("22 srt")
ax3.set_title("23 srt")
ax4.set_title("24 srt")
ax5.set_title("29 srt")
ax6.set_title("30 srt")
ax7.set_title("31 srt")
ax8.set_title("32 srt")

canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

x, y1, y2, y3, y4, y5, y6, y7, y8 = [], [], [], [], [], [], [], [], []
counter = 0
stop_graph = False


root.after(20, update_graphs)

root.mainloop()



