from ctypes import *
import tkinter as tk
from  SDK import staticIO, device, dynamic_digital, dynamic_analog
import sys
import time
import asyncio
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output
from collections import defaultdict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")


#### Открываем устройство  #######  
hdwf = c_int()
hdwf = device.open()



##### задаем положительное напряжение #############

#channel 0,1,2,3,4
for i in range(5):
    staticIO.turn_on_channel(hdwf, i)


### led pins
l_1 = 5 #data pin led
l_2 = 6 # shift pin led
l_3 = 7 # clock pin led

### struct pins
s_1 =1 # shift
s_2 =1 # clock 
s_3 =1 # data

class RealTimePlot:
    def __init__(self, root, title, xlabel, ylabel, ymin, ymax):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.ymin = ymin
        self.ymax = ymax

        self.fig, self.ax = plt.subplots()
        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.set_ylim([self.ymin, self.ymax])
        self.ax.grid(True)
        self.line, = self.ax.plot([], [])

    def update(self, x, y):
        self.line.set_data(x, y)
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        self.fig.canvas.draw()

class App:
    def __init__(self, root):
        # инициализируем графики
        self.plot1 = RealTimePlot(root, "График 1", "Время", "Значение", -10, 10)
        self.plot2 = RealTimePlot(root, "График 2", "Время", "Значение", -10, 10)
        self.plot3 = RealTimePlot(root, "График 3", "Время", "Значение", -10, 10)
        self.plot4 = RealTimePlot(root, "График 4", "Время", "Значение", -10, 10)

        # создаем кнопки для управления устройством Analog Discovery 2
        self.button1 = tk.Button(root, text="Запустить паттерн 1", command=self.pattern1)
        self.button2 = tk.Button(root, text="Запустить паттерн 2", command=self.pattern2)
        self.button3 = tk.Button(root, text="Запустить паттерн 3", command=self.pattern3)
        self.button4 = tk.Button(root, text="Запустить паттерн 4", command=self.pattern4)
        self.quit_button = tk.Button(root, text="Выход", command=root.quit)

        # располагаем элементы на окне
        self.plot1.ax.set_position([0.05, 0.05, 0.4, 0.4])
        self.plot2.ax.set_position([0.55, 0.05, 0.4, 0.4])
        self.plot3.ax.set_position([0.05, 0.55, 0.4, 0.4])
        self.plot4.ax.set_position([0.55, 0.55, 0.4, 0.4])
        self.button1.place(relx=0.05, rely=0.47, anchor="w")
        self.button2.place(relx=0.45, rely=0.47, anchor="w")
        self.button3.place(relx=0.05, rely=0.97, anchor="w")
        self.button4.place(relx=0.45, rely=0.97, anchor="w")
        self.quit_button.place(relx=0.95, rely=0.95, anchor="se")

        # запускаем измерение и обновление графиков в отдельном потоке
        self.is_running = True
        self.update_thread()
    def update_thread(self):
        while self.is_running: #считываем значения с устройства Analog Discovery 2
            struct_index: list[int] = [0 for i in range(64)]
            struct_index[21] = 1
            dynamic_analog.struct_measure(hdwf,s_1,s_2,s_3,struct_index)
            data1 = dynamic_analog.measure(hdwf,1)
            data2 = 0
            data3 = 0
            data4 = 0
            # обновляем графики
            self.plot1.update(data1[:, 0], data1[:, 1])
            self.plot2.update(data2[:, 0], data2[:, 1])
            self.plot3.update(data3[:, 0], data3[:, 1])
            self.plot4.update(data4[:, 0], data4[:, 1])
            # задержка для обновления графиков
            time.sleep(0.05)

    def pattern1(self):
        # отправляем команду на устройство Analog Discovery 2
        led_on = [1 for i in range(64)]
        dynamic_digital.led_matrix(hdwf, l_2, l_3, l_1, led_on)
        time.sleep(0.005)
        print('отправили 1 паттерн')
        

    def pattern2(self):
        # отправляем команду на устройство Analog Discovery 2
        print('отправили 2 паттерн')

    def pattern3(self):
        # отправляем команду на устройство Analog Discovery 2
        print('отправили 3 паттерн')

    def pattern4(self):
        # отправляем команду на устройство Analog Discovery 2
        print('отправили 4 паттерн')


if __name__ == "__main__":
    # создаем окно Tkinter
    root = tk.Tk()
    root.title("Real-Time Plotting with Analog Discovery 2")
    root.geometry("800x600")

    # запускаем приложение
    app = App(root)

    # запускаем главный цикл обработки событий Tkinter
    root.mainloop()

    # останавливаем измерение и обновление графиков
    app.is_running = False
