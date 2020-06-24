# !/usr/bin/python
from commons_i2c import *

# Getters pH methods


def get_slope_probe(device):
    """
    Get the pH probe slope
    @return string ?Slope,<acid closely percent of ideal probe>,<base closely percent of ideal probe>,<millivolts the zero point is off from true 0>
    """
    return device.query("Slope,?")


# Setters pH methods

def set_calibration_mid(device, solution=7.00):
    """
    Calibration the middle point
    @param float solution value
    """
    return device.query("Cal,mid,%.2f" % solution)
