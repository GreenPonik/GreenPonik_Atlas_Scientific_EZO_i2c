# !/usr/bin/python
from commons_i2c import *

# Getters EC methods


def get_k_probe(device):
    """
    get current ec probe k
    @return string ?K,<value of k>
    """
    return device.query("K,?")


def get_ouput_parameters(device):
    """
    Get the current list of parameters a returned when call read method
    EC = electro conductivity µS/cm
    TDS = total dissolved solids ppm
    S = salinity PSU (ppt)
    SG = specific gravity
    @return string ?,O,EC,TDS,S,SG for all enabled
    if "no output" is returned all parameters are disabled
    """
    return device.query("O,?")

# Setters EC methods


def set_k_probe(device, k):
    """
    Set the ec probe k
    @param k float the probe k
    """
    return device.query("K,%.2f" % k)


def set_calibration_dry(device):
    """
    Set the calibration of probe in the air
    """
    return device.query("Cal,dry")


def set_calibration_one_point(device, point):
    """
    One point calibration
    @param float or int point to calibrate
    """
    return device.query("Cal,%d" % point)


def set_output_parameter(device, param, state):
    """
    define the output string of read method
    @param string EC/TDS/S/SG
    @param state int or bool 1 = enable / 0 = disable
    """
    return device.query("O,%s,%d" % (param, state,))
