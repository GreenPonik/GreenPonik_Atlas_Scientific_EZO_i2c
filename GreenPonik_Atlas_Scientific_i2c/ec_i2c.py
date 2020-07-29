# !/usr/bin/python
# import commons_i2c

# Getters EC methods


def get_k_probe(device):
    """
    @brief Get current ec probe k
    @param AtlasI2c instance
    @return string ?K,<value of k>
    """
    return device.query("K,?")


def get_ouput_parameters(device):
    """
    @brief Get the current list of parameters a returned when call read method
    EC = electro conductivity µS/cm
    TDS = total dissolved solids ppm
    S = salinity PSU (ppt)
    SG = specific gravity
    @param AtlasI2c instance
    @return string ?,O,EC,TDS,S,SG for all enabled
    if "no output" is returned all parameters are disabled
    """
    return device.query("O,?")

# Setters EC methods


def set_k_probe(device, k):
    """
    @brief Set the ec probe k
    @param AtlasI2c instance
    @param k float the probe k
    """
    return device.query("K,%.2f" % k)


def set_calibration_dry(device):
    """
    @biref Set the calibration of probe in the air
    @param AtlasI2c instance
    """
    return device.query("Cal,dry")


def set_calibration_one_point(device, point):
    """
    @brief One point calibration
    @param AtlasI2c instance
    @param float or int point to calibrate
    """
    return device.query("Cal,%d" % point)


def set_output_parameter(device, param, state):
    """
    @brief define the output string of read method
    @param string EC/TDS/S/SG
    @param state int or bool 1 = enable / 0 = disable
    """
    return device.query("O,%s,%d" % (param, state,))
