#! /usr/bin/python3

"""
@package Class to communicate with Atlas Scientific sensors in I2C mode.
####################################################################
####################################################################
####################################################################
##################### Atlas Scientific i2c #########################
######################### by GreenPonik ############################
####################################################################
####################################################################
####################################################################
Source code is based on Atlas Scientific documentations:
https://www.atlas-scientific.com/files/EC_EZO_datasheet.pdf
https://atlas-scientific.com/files/EZO_pH_datasheet.pdf
"""
from GreenPonik_Atlas_Scientific_EZO_i2c.GreenPonik_CommonsI2c import _CommonsI2c


class PHI2c(_CommonsI2c):
    """
    @brief specific methods for EZO PH module
    """

    # ----- Getters pH methods ----- ######

    def get_slope_probe(self):
        """
        @brief Get the pH probe slope
        @param AtlasI2c instance
        @return string ?Slope,<acid closely percent of ideal probe>,
        <base closely percent of ideal probe>,
        <millivolts the zero point is off from true 0>
        """
        return self._device.query("Slope,?")

    # ----- Setters pH methods ----- ######
