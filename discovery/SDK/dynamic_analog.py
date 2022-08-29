""" DEVICE CONTROL FUNCTIONS: open, check_error, close """

import sys
from ctypes import *
from dwfconstants import DwfDigitalOutTypeCustom
import time

"""-----------------------------------------------------------------------"""

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

hzSys = c_double()
"""-----------------------------------------------------------------------"""

#Analog to digital

def measure(device_handle,channel):
     """
        measure a voltage
        parameters: - device data
                    - the selected oscilloscope channel (1-2, or 1-4)
 
        returns:    - the measured voltage in Volts
    """"
    
    # set up the instrument
    dwf.FDwfAnalogInConfigure(device_data.handle, c_bool(False), c_bool(False))
 
    # read data to an internal buffer
    dwf.FDwfAnalogInStatus(device_data.handle, c_bool(False), c_int(0))
 
    # extract data from that buffer
    voltage = c_double()   # variable to store the measured voltage
    dwf.FDwfAnalogInStatusSample(device_data.handle, c_int(channel - 1), byref(voltage))
 
    # store the result as float
    voltage = voltage.value
    return voltage
    




 


    
