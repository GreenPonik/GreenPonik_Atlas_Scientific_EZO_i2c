# !/usr/bin/python

from atlas_ezo_i2c import AtlasEzoI2c

# Getters commons methods


def get_device_info(device):
    """
    Get device information
    @return device name, firmware version
    """
    return device.query("i")


def get_read(device):
    """
    Read sensor value
    @return string (depending of O parameter for EZO EC)
    """
    return device.query("R")


def get_temperature(device):
    """
    Get current compensation temperature
    @return string ?T,<temperature value>
    """
    return device.query("T,?")


def get_calibration(device):
    """
    Get current calibrations data
    """
    return device.query("Cal,?")


def get_find(device):
    """
    Fin devices
    @return  OK
    """
    return device.query("Find")


def get_status(device):
    """
    Get EZO status
    @return status of device decode them by using AtlasEzoI2c.AS_RESTART_CODES
    """
    return device.query("Status")


def get_led(device):
    """
    Get led state
    @return string ?L,1 for On / ?L,0 for Off
    """
    return device.query("L,?")


def get_plock(device):
    """
    Get Plock status
    @return string ?Plock,1 for Locked / ?L,0 for Unlocked
    """
    return device.query("Plock,?")


# Setters commons methods


def set_temperature(device, t=25.0):
    """
    Set the compensation temperature
    @param float temperature value
    """
    return device.query("T,%.2f" % t)


def set_calibration_low(device, solution=0.0):
    """
    calibration 2 points low point 
    @param float
    """
    return device.query("Cal,low,%.2f" % solution)


def set_calibration_high(device, solution=0.0):
    """
    calibration 2 points high point 
    @param float
    """
    return device.query("Cal,high,%.2f" % solution)


def set_calibration_clear(device):
    return device.query("Cal,clear")


def set_i2c_addr(device, add):
    """
    Change the device i2c address
    @param int add
    """
    if not isinstance(add, int):
        return "only decimal address expected, convert hexa by using AtlasEzoI2c.AS_SENSORS_ADDS_HEXA_TO_DECIMAL"
    else:
        if add not in AtlasEzoI2c.AS_SENSORS_ADDS_DECIMAL:
            return "cannot use this i2c address %d check AtlasEzoI2c.AS_SENSORS_ADDS_DECIMAL" % add
        else:
            return device.query("I2C,%d" % add)


def set_led(device, state=1):
    """
    Change Led state
    @param int or bool state = 1 = On / state = 0 = Off 
    """
    return device.query("L,%d" % state)


def set_sleep_mode(device):
    """
    Enter sleep mode / low power
    """
    return device.query("Sleep")


def set_facory(device):
    """
    Factory reset, clears calibration, LED on, Response codes enabled
    """
    return device.query("Factory")


def set_plock(device, state):
    """
    Plock is used to lock the changes between I2C and UART
    @param int or bool state = 1 = Locked / state = 0 = Unlocked
    """
    return device.query("Plock, %d" % state)


if __name__ == "__main__":
    ezo_ec = AtlasEzoI2c(
        address=AtlasEzoI2c.AS_SENSORS_ADDS_TXT_TO_DECIMAL['EC'],
        moduletype="EC",
        name="EC")
    print(">>>get ezo ec information")
    print(get_device_info(ezo_ec))
