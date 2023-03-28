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

hdwf = c_int()
hdwf = device.open()

led_off = [0 for i in range(64)]
led_on = [1 for i in range(64)]
dynamic_digital.led_matrix(hdwf, 1, 2, 0, led_off) # выключаем светодиоды

struct_index = [0 for i in range(64)]
struct_index[6] = 1
dynamic_analog.struct_measure(hdwf, 4, 5, 6, struct_index) # struct_measure(device_handle,shift,clock,data,matrix)

def measure():
    return dynamic_analog.measure(hdwf,1)

def some_function():
    print("Выполняется функция, не связанная с графиком")

def close():
    print("Закрытие программы")

def update_graphs():
    global x, y1, y2,  y3 ,y4, counter

    if not stop_graph:
        x.append(counter)
        y1.append(measure())
        y2.append(measure())
        y3.append(measure())
        y4.append(measure())
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

        root.after(50, update_graphs)

def stop():
    global stop_graph
    stop_graph = True
    close()
    root.quit()

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
ax3.set_title("21 место")
ax4.set_title(" 22 место")


canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

x, y1, y2, y3,y4 = [], [], [],[],[]
counter = 0
stop_graph = False

root.after(50, update_graphs)
root.mainloop()