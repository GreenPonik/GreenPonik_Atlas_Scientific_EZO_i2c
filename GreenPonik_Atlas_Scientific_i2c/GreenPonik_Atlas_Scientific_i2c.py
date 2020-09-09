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
Source code is based on examples from Atlas Scientific:
https://github.com/AtlasScientific/Raspberry-Pi-sample-code/blob/master/AtlasI2C.py
"""

import io
import sys
import fcntl
import time
import copy

# import adafruit_bus_device.i2c_device as i2c_device
# from adafruit_extended_bus import ExtendedI2C as I2C
# from Adafruit_PureIO import smbus

# class AtlasI2c:
#
#     def __init__(self, address=None, moduletype="", name="", bus=None):
#         """
#         open two file streams, one for reading and one for writing
#         the specific I2C channel is selected with bus
#         it is usually 1, except for older revisions where its 0
#         wb and rb indicate binary read and write
#         """
#         self._address = address or self.DEFAULT_ADDR
#         self.bus = bus or self.DEFAULT_BUS
#         self._long_timeout = self.LONG_TIMEOUT
#         self._short_timeout = self.SHORT_TIMEOUT
#         self.file_read = io.open(file="/dev/i2c-{}".format(self.bus),
#                                  mode="rb",
#                                  buffering=0)
#         self.file_write = io.open(file="/dev/i2c-{}".format(self.bus),
#                                   mode="wb",
#                                   buffering=0)
#         self.set_i2c_address(self._address)
#         self._name = name
#         self._module = moduletype

#     @property
#     def long_timeout(self):
#         return self._long_timeout

#     @property
#     def short_timeout(self):
#         return self._short_timeout

#     @property
#     def name(self):
#         return self._name

#     @property
#     def address(self):
#         return self._address

#     @property
#     def moduletype(self):
#         return self._module

#     def set_i2c_address(self, addr):
#         """
#         @brief set the I2C communications to the slave specified by the address
#         the commands for I2C dev using the ioctl functions are specified in
#         the i2c-dev.h file from i2c-tools
#         """
#         I2C_SLAVE = 0x703
#         fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
#         fcntl.ioctl(self.file_write, I2C_SLAVE, addr)
#         self._address = addr

#     def write(self, cmd):
#         """
#         @brief appends the null character and sends the string over I2C
#         """
#         cmd += "\00"
#         self.file_write.write(cmd.encode('latin-1'))

#     def handle_raspi_glitch(self, response):
#         """
#         @brief Change MSB to 0 for all received characters except the first
#         and get a list of characters
#         NOTE: having to change the MSB to 0 is a glitch in the raspberry pi,
#         and you shouldn't have to do this!
#         """
#         if self.app_using_python_two():
#             return list(map(lambda x: chr(ord(x) & ~0x80), list(response)))
#         else:
#             return list(map(lambda x: chr(x & ~0x80), list(response)))

#     def app_using_python_two(self):
#         return sys.version_info[0] < 3

#     def get_response(self, raw_data):
#         if self.app_using_python_two():
#             response = [i for i in raw_data if i != '\x00']
#         else:
#             response = raw_data

#         return response

#     def response_valid(self, response):
#         valid = True
#         error_code = None
#         if(len(response) > 0):

#             if self.app_using_python_two():
#                 error_code = str(ord(response[0]))
#             else:
#                 error_code = str(response[0])

#             if error_code != '1':  # 1:
#                 valid = False

#         return valid, error_code

#     def get_device_info(self):
#         """
#         @brief get the device info
#         @return string moduletype address name
#         """
#         if(self._name == ""):
#             return self._module + " " + str(self.address)
#         else:
#             return self._module + " " + str(self.address) + " " + self._name

#     def read(self, num_of_bytes=31):
#         """
#         @brief reads a specified number of bytes from I2C,
#         then parses and displays the result
#         """
#         raw_data = self.file_read.read(num_of_bytes)
#         response = self.get_response(raw_data=raw_data)
#         # print(response)
#         is_valid, error_code = self.response_valid(response=response)

#         if is_valid:
#             char_list = self.handle_raspi_glitch(response[1:])
#             # result = "Success " + self.get_device_info()
#             # + ": "
#             # + str(''.join(char_list))
#             # result = "Success: " +  str(''.join(char_list))
#             result = "Success %s: %s" % (
#                 self.get_device_info(),
#                 str(''.join(char_list))
#             )
#         else:
#             result = "Error " + self.get_device_info() + ": " + error_code

#         return result

#     def get_command_timeout(self, command):
#         timeout = None
#         if command.upper().startswith(self.LONG_TIMEOUT_COMMANDS):
#             timeout = self._long_timeout
#         elif not command.upper().startswith(self.SLEEP_COMMANDS):
#             timeout = self.short_timeout

#         return timeout

#     def query(self, command):
#         """
#         @brief write a command to the board, wait the correct timeout,
#         and read the response
#         """
#         self.write(command)
#         current_timeout = self.get_command_timeout(command=command)
#         if not current_timeout:
#             return "sleep mode"
#         else:
#             time.sleep(current_timeout)
#             return self.read()

#     def close(self):
#         self.file_read.close()
#         self.file_write.close()

#     def list_i2c_devices(self):
#     """
#     @brief save the current address so we can restore it after
#     """
#     prev_addr = copy.deepcopy(self._address)
#     i2c_devices = []
#     for i in range(0, 128):
#         try:
#             self.set_i2c_address(i)
#             self.read(1)
#             i2c_devices.append(i)
#         except IOError:
#             pass
#     # restore the address we were using
#     self.set_i2c_address(prev_addr)

#     return i2c_devices


class AtlasI2c:
    """@brief
    Array key=>value for each EZO sensors i2c hexa addresses
    """
    ADDR_EZO_HEXA = {
        0x61,  # DO
        0x62,  # ORP
        0x63,  # PH
        0x64,  # EC
    }
    """@brief
    Array value of each EZO sensors i2c decimal addresses
    """
    ADDR_EZO_DECIMAL = {
        97,   # DO
        98,   # ORP
        99,   # PH
        100,  # EC
    }
    """@brief
    Array key=>value for each EZO sensors name i2c hexa addresses
    """
    ADDR_EZO_TXT_TO_HEXA = {
        'DO': 0x61,
        'ORP': 0x62,
        'PH': 0x63,
        'EC': 0x64,
    }
    """@brief
    Array key=>value for each EZO sensors i2c hexa to decimal addresses
    """
    ADDR_EZO_HEXA_TO_DECIMAL = {
        0x61: 97,   # DO
        0x62: 98,   # ORP
        0x63: 99,   # PH
        0x64: 100,  # EC
    }
    """@brief
    Array key=>value for each OEM sensors i2c hexa addresses
    """
    ADDR_OEM_HEXA = {
        0x64,  # EC
        0x65,  # PH
        0x66,  # ORP
        0x67,  # DO
    }
    """@brief
    Array value of each OEM sensors decimal addresses
    """
    ADDR_OEM_DECIMAL = {
        100,   # EC
        101,   # PH
        102,   # ORP
        103,   # DO
    }
    """@brief
    Array key=>value for each OEM sensors name i2c hexa addresses
    """
    ADDR_OEM_TXT_TO_HEXA = {
        'EC': 0x64,
        'PH': 0x65,
        'ORP': 0x66,
        'DO': 0x67,
    }
    """@brief
    Array key=>value for each OEM sensors i2c hexa to decimal addresses
    """
    ADDR_OEM_HEXA_TO_DECIMAL = {
        0x64: 100,   # DO
        0x65: 101,   # ORP
        0x66: 102,   # PH
        0x67: 103,  # EC
    }

    # TODO don't give a default address and provide an error when nothing is provided
    # the default address for the sensor
    DEFAULT_ADDR = 100
    # the default bus for I2C on the newer Raspberry Pis,
    # certain older boards use bus 0
    DEFAULT_BUS = 1

    # the timeout needed to query readings and calibrations
    LONG_TIMEOUT = 1.5
    # timeout for regular commands
    SHORT_TIMEOUT = .3

    LONG_TIMEOUT_COMMANDS = ("R", "CAL")
    SLEEP_COMMANDS = ("SLEEP", )

    @property
    def bus(self):
        return self._bus

    @bus.setter
    def bus(self, bus_number):
        self._bus = bus_number

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    @property
    def short_timeout(self):
        return self._short_timeout

    @short_timeout.setter
    def short_timeout(self, timeout):
        self._short_timeout = timeout

    @property
    def long_timeout(self):
        return self._long_timeout

    @long_timeout.setter
    def long_timeout(self, timeout):
        self._long_timeout = timeout

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        self._name = n

    @property
    def module(self):
        return self._module

    @module.setter
    def module(self, m):
        self._module = m

    def __init__(self, bus=DEFAULT_BUS, addr=DEFAULT_ADDR, moduletype="", name=""):
        """
        open two file streams, one for reading and one for writing
        the specific I2C channel is selected with bus
        it is usually 1, except for older revisions where its 0
        wb and rb indicate binary read and write
        """
        # private properties
        self._bus = bus
        self._address = addr
        self._name = name
        self._module = moduletype
        self._short_timeout = self.SHORT_TIMEOUT
        self._long_timeout = self.LONG_TIMEOUT

        # public properties
        self.file_read = io.open(file="/dev/i2c-{}".format(self._bus),
                                 mode="rb",
                                 buffering=0)
        self.file_write = io.open(file="/dev/i2c-{}".format(self._bus),
                                  mode="wb",
                                  buffering=0)
        """
        @brief set the I2C communications to the slave specified by the address
        the commands for I2C dev using the ioctl functions are specified in
        the i2c-dev.h file from i2c-tools
        """
        I2C_SLAVE = 0x703
        fcntl.ioctl(self.file_read, I2C_SLAVE, self._address)
        fcntl.ioctl(self.file_write, I2C_SLAVE, self._address)

    def get_command_timeout(self, command):
        timeout = None
        if command.upper().startswith(self.LONG_TIMEOUT_COMMANDS):
            timeout = self._long_timeout
        elif not command.upper().startswith(self.SLEEP_COMMANDS):
            timeout = self.short_timeout

        return timeout

    def query(self, command):
        """
        @brief write a command to the board, wait the correct timeout,
        and read the response
        """
        self.write(command)
        current_timeout = self.get_command_timeout(command=command)
        if not current_timeout:
            return "sleep mode"
        else:
            time.sleep(current_timeout)
            return self.read()

    def read(self, num_of_bytes=31):
        # reads a specified number of bytes from I2C, then parses and displays the result
        res = self.file_read.read(num_of_bytes)         # read from the board
        response = list(filter(lambda x: x != '\x00', res))     # remove the null characters to get the response
        print(response)
        if response[0] == 1:             # if the response isn't an error
            # change MSB to 0 for all received characters except the first and get a list of characters
            char_list = map(lambda x: chr(x & ~0x80), list(response[1:]))
            # NOTE: having to change the MSB to 0 is a glitch in the raspberry pi, and you shouldn't have to do this!
            return "Command succeeded " + ''.join(char_list)     # convert the char list to a string and returns it
        else:
            return "Error " + str(response[0])

    def write(self, cmd):
        # appends the null character and sends the string over I2C
        cmd += "\00"
        print(cmd)
        self.file_write.write(cmd.encode('latin-1'))

    def close(self):
        self.file_read.close()
        self.file_write.close()

    def list_i2c_devices(self):
        """
        @brief save the current address so we can restore it after
        """
        prev_addr = copy.deepcopy(self._address)
        i2c_devices = []
        for i in range(0, 128):
            try:
                self.address(i)
                self.read(1)
                i2c_devices.append(i)
            except IOError:
                pass
        # restore the address we were using
        self.address(prev_addr)

        return i2c_devices


class _CommonsI2c:

    def __init__(self, device):
        self._device = device

    """
    Getters commons methods
    """
    def get_device_info(self):
        """
        @brief Get device information
        @param device = AltasI2c instance
        @return device name, firmware version
        """
        return self._device.query("i")

    def get_read(self):
        """
        @brief Read sensor value
        @param device = AltasI2c instance
        @return string (depending of O parameter)
        """
        return self._device.query("R")

    def get_temperature(self):
        """
        @brief Get current compensation temperature
        @param device = AltasI2c instance
        @return string ?T,<temperature value>
        """
        return self._device.query("T,?")

    def get_calibration(self):
        """
        @brief Get current calibrations data
        @param device = AltasI2c instance
        @return ?CAL,<current calibration>
        """
        return self._device.query("Cal,?")

    def get_find(self):
        """
        @brief Fin devices
        @param device = AltasI2c instance
        @return OK
        """
        return self._device.query("Find")

    def get_status(self):
        """
        @brief Get status
        @param device = AltasI2c instance
        @return status of device decode them by using AtlasI2c.AS_RESTART_CODES
        """
        return self._device.query("Status")

    def get_led(self):
        """
        @brief Get led state
        @param device = AltasI2c instance
        @return string ?L,1 for On / ?L,0 for Off
        """
        return self._device.query("L,?")

    def get_plock(self):
        """
        @brief Get Plock status
        @param device = AltasI2c instance
        @return string ?Plock,1 for Locked / ?L,0 for Unlocked
        """
        return self._device.query("Plock,?")

    """ Setters commons methods
    """
    def set_temperature(self, t=25.0):
        """
        @brief Set the compensation temperature
        @param device = AltasI2c instance
        @param t = float temperature value
        """
        return self._device.query("T,%.2f" % t)

    def set_calibration_low(self, solution=0.0):
        """
        @brief calibration 2 points low point
        @param device = AltasI2c instance
        @param float = low solution calibration
        """
        return self._device.query("Cal,low,%.2f" % solution)

    def set_calibration_high(self, solution=0.0):
        """
        @brief calibration 2 points high point
        @param device = AltasI2c instance
        @param float = high solution calibration
        """
        return self._device.query("Cal,high,%.2f" % solution)

    def set_calibration_clear(self):
        """
        @brief Clear calibration data
        @param device = AltasI2c instance
        """
        return self._device.query("Cal,clear")

    def set_i2c_addr(self, add):
        """
        @brief Change the device i2c address
        @param device = AltasI2c instance
        @param int = new i2c add
        """
        if not isinstance(add, int):
            return "only decimal address expected, convert hexa by using \
                AtlasI2c.ADDR_OEM_DECIMAL or AtlasI2c.ADDR_EZO_DECIMAL"
        else:
            if(add not in AtlasI2c.ADDR_OEM_DECIMAL
                and add not in AtlasI2c.ADDR_EZO_DECIMAL
               ):
                return "cannot use this i2c address %d check \
                    AtlasI2c.ADDR_OEM_DECIMAL or AtlasI2c.ADDR_EZO_DECIMAL" % add
            else:
                self._device.address(add)
                return self._device.query("I2C,%d" % add)

    def set_led(self, state=1):
        """
        @brief Change Led state
        @param device = AltasI2c instance
        @param int or bool state = 1 = On / state = 0 = Off
        """
        return self._device.query("L,%d" % state)

    def set_sleep_mode(self):
        """
        @brief Enter sleep mode / low power
        @param device = AltasI2c instance
        """
        return self._device.query("Sleep")

    def set_facory(self):
        """
        @brief Factory reset, clears calibration, LED on,
        Response codes enabled
        @param device = AltasI2c instance
        """
        return self._device.query("Factory")

    def set_plock(self, state):
        """
        @brief Plock is used to lock the changes between I2C and UART
        @param device = AltasI2c instance
        @param int or bool state = 1 = Locked / state = 0 = Unlocked
        """
        return self._device.query("Plock, %d" % state)


class ECI2c(_CommonsI2c):
    """
    @brief specific methods for EZO EC module
    """
    """ Getters EC methods
    """
    def get_k_probe(self):
        """
        @brief Get current ec probe k
        @param AtlasI2c instance
        @return string ?K,<value of k>
        """
        return self._device.query("K,?")

    def get_ouput_parameters(self):
        """
        @brief Get the current list of parameters has returned
        when call read method
        EC = electro conductivity µS/cm
        TDS = total dissolved solids ppm
        S = salinity PSU (ppt)
        SG = specific gravity
        @param AtlasI2c instance
        @return string ?,O,EC,TDS,S,SG for all enabled
        if "no output" is returned all parameters are disabled
        """
        return self._device.query("O,?")

    """
    Setters EC methods
    """
    def set_k_probe(self, k):
        """
        @brief Set the ec probe k
        @param AtlasI2c instance
        @param k float the probe k
        """
        return self._device.query("K,%.2f" % k)

    def set_calibration_dry(self):
        """
        @biref Set the calibration of probe in the air
        @param AtlasI2c instance
        """
        return self._device.query("Cal,dry")

    def set_calibration_one_point(self, point):
        """
        @brief One point calibration
        @param AtlasI2c instance
        @param float or int point to calibrate
        """
        return self._device.query("Cal,%d" % point)

    def set_output_parameter(self, param, state):
        """
        @brief define the output string of read method
        @param string EC/TDS/S/SG
        @param state int or bool 1 = enable / 0 = disable
        """
        return self._device.query("O,%s,%d" % (param, state,))


class PHI2c(_CommonsI2c):
    """
    @brief specific methods for EZO PH module
    """
    """ Getters pH methods
    """
    def get_slope_probe(self):
        """
        @brief Get the pH probe slope
        @param AtlasI2c instance
        @return string ?Slope,<acid closely percent of ideal probe>,
        <base closely percent of ideal probe>,
        <millivolts the zero point is off from true 0>
        """
        return self._device.query("Slope,?")

    """ Setters pH methods
    """
    def set_calibration_mid(self, solution=7.00):
        """
        @brief Calibration the middle point
        @param AtlasI2c instance
        @param float solution value
        """
        return self._device.query("Cal,mid,%.2f" % solution)
