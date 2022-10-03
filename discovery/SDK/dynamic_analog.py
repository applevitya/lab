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
    
    """
    
    # set up the instrument
    dwf.FDwfAnalogInConfigure(device_handle, c_bool(False), c_bool(False))
 
    # read data to an internal buffer
    dwf.FDwfAnalogInStatus(device_handle, c_bool(False), c_int(0))
 
    # extract data from that buffer
    voltage = c_double()   # variable to store the measured voltage
    dwf.FDwfAnalogInStatusSample(device_handle, c_int(channel - 1), byref(voltage))
 
    # store the result as float
    voltage = voltage.value
    return voltage
    

def osc(device_data,param, channel):
    '''
    param=[sampling_frequency,buffer_size,offset,amplitude_range]
    '''
    #initialize osc
    dwf.FDwfAnalogInChannelEnableSet(device_data.handle, c_int(0), c_bool(True))
    dwf.FDwfAnalogInChannelOffsetSet(device_data.handle, c_int(0), c_double(param[2]))
    dwf.FDwfAnalogInChannelRangeSet(device_data.handle, c_int(0), c_double(param[3]))
    dwf.FDwfAnalogInBufferSizeSet(device_data.handle, c_int(param[1]))
    dwf.FDwfAnalogInFrequencySet(device_data.handle, c_double(param[0]))
    dwf.FDwfAnalogInChannelFilterSet(device_data.handle, c_int(-1), constants.filterDecimate)
    
    #record
    
    dwf.FDwfAnalogInConfigure(device_data.handle, c_bool(False), c_bool(True))
    
    while True:
        status = ctypes.c_byte()    # variable to store buffer status
        dwf.FDwfAnalogInStatus(device_data.handle, ctypes.c_bool(True), ctypes.byref(status))
 
        
        if status.value == constants.DwfStateDone.value:
                # exit loop when ready
                break
 
    buffer = (ctypes.c_double * data.buffer_size)()   # create an empty buffer
    dwf.FDwfAnalogInStatusData(device_data.handle, ctypes.c_int(channel - 1), buffer, ctypes.c_int(data.buffer_size))
 

    time = range(0, data.buffer_size)
    time = [moment / data.sampling_frequency for moment in time]
 

    buffer = [float(element) for element in buffer]
    
    return buffer,time
 


    
