from ctypes import *
from  SDK import staticIO, device, dynamic_digital, dynamic_analog
import sys
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time
import random


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
dynamic_digital.led_matrix(hdwf,1,2,0,led_off) # выключаем светодиоды

struct_index = [0 for i in range(64)]
struct_index[6] = 1
dynamic_analog.struct_measure(hdwf,4,5,6,struct_index) # struct_measure(device_handle,shift,clock,data,matrix)

def measure():
    # Здесь ваша функция measure, которая возвращает число
    return dynamic_analog.measure(hdwf,1)


def on_button_click():
    dynamic_digital.led_matrix(hdwf, 1, 2, 0, led_on)
    time.sleep(0.05)
    dynamic_digital.led_matrix(hdwf, 1, 2, 0, led_off)
    pass


def close(root):
    dwf.FDwfDigitalOutReset(hdwf)
    device.close(hdwf)
    root.quit()
    root.destroy()


def update_plot(plot, canvas):
    while True:
        data = measure()
        plot.set_ydata(np.append(plot.get_ydata()[1:], data))
        canvas.draw()
        time.sleep(0.0005)


def main():
    root = tk.Tk()
    root.title("Real-time Plot")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0)

    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Real-time Data")
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")

    line, = ax.plot(np.zeros(100))

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)

    button_execute = ttk.Button(frame, text="Execute Function", command=on_button_click)
    button_execute.grid(row=1, column=0)

    button_quit = ttk.Button(frame, text="Close", command=lambda: close(root))
    button_quit.grid(row=2, column=0)

    update_thread = threading.Thread(target=update_plot, args=(line, canvas))
    update_thread.start()

    root.mainloop()


if __name__ == "__main__":
    main()
