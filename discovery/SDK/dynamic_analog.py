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





 


    
