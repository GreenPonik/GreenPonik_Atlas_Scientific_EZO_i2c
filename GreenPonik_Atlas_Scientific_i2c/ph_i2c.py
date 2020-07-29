# !/usr/bin/python
# import commons_i2c

# Getters pH methods


def get_slope_probe(device):
    """
    @brief Get the pH probe slope
    @param AtlasI2c instance
    @return string ?Slope,<acid closely percent of ideal probe>,
    <base closely percent of ideal probe>,
    <millivolts the zero point is off from true 0>
    """
    return device.query("Slope,?")


# Setters pH methods

def set_calibration_mid(device, solution=7.00):
    """
    @brief Calibration the middle point
    @param AtlasI2c instance
    @param float solution value
    """
    return device.query("Cal,mid,%.2f" % solution)
