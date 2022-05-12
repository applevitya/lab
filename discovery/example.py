"""
   DWF Python Example
   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
from  SDK import staticIO, device, dynamic_digital
import sys
import time

import asyncio

if sys.platform.startswith("win"):
    dwf = ctypes.cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")


    
hdwf = ctypes.c_int()
hdwf = device.open()

# channel 0 - clock
# channel 1 - shift
# channel 2 - data
# channel 3 - reset



hdwf = c_int()

version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))


print("Opening first device")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == 0:
    print("failed to open device")
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(str(szerr.value))
    quit()

print("Configuring Digital Out")

hzSys = c_double()
dwf.FDwfDigitalOutInternalClockInfo(hdwf, byref(hzSys))


data_py = [1,0,1,0,1,0,1,0,1,0]

for i in range(246): data_py.append(1)


data_py2 = [0,1,0,1,0,1,0,1,0,1]

for i in range(246): data_py2.append(0)

# how many bytes we need to fit this many bits, (+7)/8
rgbdata=(c_ubyte*((len(data_py)+7)>>3))(0)

# array to bits in byte array
for i in range(len(data_py)):
    if data_py[i] != 0:
        rgbdata[i>>3] |= 1<<(i&7)


rgbdata2=(c_ubyte*((len(data_py2)+7)>>3))(0)
# array to bits in byte array
for i in range(len(data_py2)):
    if data_py2[i] != 0:
        rgbdata2[i>>3] |= 1<<(i&7)



pin=0
pin1 = 1
# generate pattern
dwf.FDwfDigitalOutRunSet(hdwf, c_double(0.0005)) # 1ms run
dwf.FDwfDigitalOutEnableSet(hdwf, c_int(pin), c_int(1))


dwf.FDwfDigitalOutTypeSet(hdwf, c_int(pin), DwfDigitalOutTypeCustom)
# 100kHz sample rate
dwf.FDwfDigitalOutIdleSet(hdwf, c_int(0), c_int(1))
dwf.FDwfDigitalOutDividerSet(hdwf, c_int(pin), c_int(int(hzSys.value/(2*128e3)))) # set sample rate
dwf.FDwfDigitalOutDataSet(hdwf, c_int(pin), byref(rgbdata), c_int(len(data_py)))
dwf.FDwfDigitalOutCounterInitSet(hdwf, c_int(0), c_int(1), c_int(0)) # initialize high on start


########################

# generate pattern
dwf.FDwfDigitalOutRunSet(hdwf, c_double(0.0005)) # 1ms run
dwf.FDwfDigitalOutEnableSet(hdwf, c_int(pin1), c_int(1))


dwf.FDwfDigitalOutTypeSet(hdwf, c_int(pin1), DwfDigitalOutTypeCustom)
# 100kHz sample rate
dwf.FDwfDigitalOutIdleSet(hdwf, c_int(0), c_int(1))
dwf.FDwfDigitalOutDividerSet(hdwf, c_int(pin1), c_int(int(hzSys.value/(2*128e3)))) # set sample rate
dwf.FDwfDigitalOutDataSet(hdwf, c_int(pin1), byref(rgbdata2), c_int(len(data_py2)))
dwf.FDwfDigitalOutCounterInitSet(hdwf, c_int(0), c_int(1), c_int(0)) # initialize high on start




##########################



print("Generating pattern...")
dwf.FDwfDigitalOutConfigure(hdwf, c_int(1))

time.sleep(1)

pcount = c_int()
dwf.FDwfDigitalOutDataInfo(hdwf,c_int(pin),byref(pcount))

print(len(data_py))
dwf.FDwfDigitalOutReset(hdwf)
dwf.FDwfDeviceCloseAll()







dwf.FDwfDigitalOutReset(hdwf)

device.close(hdwf)




