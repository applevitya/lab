import numpy
import math
 
#генерируем массив значений для сигнала LED с частотой дискретизации dt и время наблюдения t
t = 100000 #ms
dt = 10    #ms

led = []
for i in range(int(t/dt)):
    led.append(0)
    
def led_pulses(tau,T,N):
    for i in range(int(t/dt)):
        
    
    
