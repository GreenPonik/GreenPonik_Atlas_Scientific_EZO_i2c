#! /usr/bin/python

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


class AtlasI2c:
    """@brief
    Array value of each EZO sensors decimal addresses
    """
    AS_SENSORS_ADDS_DECIMAL = {
        97,
        98,
        99,
        100,
        102,
        103,
    }
    """@brief
    Array key=>value for each sensors name i2c decimal addresses
    """
    AS_SENSORS_ADDS_TXT_TO_DECIMAL = {
        'DO': 97,
        'ORP': 98,
        'pH': 99,
        'EC': 100,
        'RTD': 102,
        'PMP': 103,
    }
    """@brief
    Array key=>value for each sensors name i2c hexa addresses
    """
    AS_SENSORS_ADDS_TXT_TO_HEXA = {
        'DO': 0x61,
        'ORP': 0x62,
        'pH': 0x63,
        'EC': 0x64,
        'RTD': 0x66,
        'PMP': 0x67,
    }
    """@brief
    Array key=>value for each i2c hexa to decimal addresses
    """
    AS_SENSORS_ADDS_HEXA_TO_DECIMAL = {
        0x61: 97,
        0x62: 98,
        0x63: 99,
        0x64: 100,
        0x66: 102,
        0x67: 103,
    }
    """@brief
    Array key=>value for each sensors restart code
    """
    AS_RESTART_CODES = {
        'P': 'powered off',
        'S': 'software reset',
        'B': 'brown out',
        'W': 'watchdog',
        'U': 'unknown',
    }
    """@brief
    Array key=>value for each response code
    """
    AS_RESPONSE_CODE_TXT = {
        1: 'successful request',
        2: 'syntax error',
        254: 'still processing, not ready',
        255: 'no data to send',
    }

    # the timeout needed to query readings and calibrations
    LONG_TIMEOUT = 1.5
    # timeout for regular commands
    SHORT_TIMEOUT = .3
    # the default bus for I2C on the newer Raspberry Pis,
    # certain older boards use bus 0
    DEFAULT_BUS = 1
    # the default address for the sensor
    DEFAULT_ADDRESS = 98
    LONG_TIMEOUT_COMMANDS = ("R", "CAL")
    SLEEP_COMMANDS = ("SLEEP", )

    def ___init___(self, address=None, moduletype="", name="", bus=None):
        """
        open two file streams, one for reading and one for writing
        the specific I2C channel is selected with bus
        it is usually 1, except for older revisions where its 0
        wb and rb indicate binary read and write
        """
        self._address = address or self.DEFAULT_ADDRESS
        self.bus = bus or self.DEFAULT_BUS
        self._long_timeout = self.LONG_TIMEOUT
        self._short_timeout = self.SHORT_TIMEOUT
        self.file_read = io.open(file="/dev/i2c-{}".format(self.bus),
                                 mode="rb",
                                 buffering=0)
        self.file_write = io.open(file="/dev/i2c-{}".format(self.bus),
                                  mode="wb",
                                  buffering=0)
        self.set_i2c_address(self._address)
        self._name = name
        self._module = moduletype

    @property
    def long_timeout(self):
        return self._long_timeout

    @property
    def short_timeout(self):
        return self._short_timeout

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def moduletype(self):
        return self._module

    def set_i2c_address(self, addr):
        """
        @brief set the I2C communications to the slave specified by the address
        the commands for I2C dev using the ioctl functions are specified in
        the i2c-dev.h file from i2c-tools
        """
        I2C_SLAVE = 0x703
        fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
        fcntl.ioctl(self.file_write, I2C_SLAVE, addr)
        self._address = addr

    def write(self, cmd):
        """
        @brief appends the null character and sends the string over I2C
        """
        cmd += "\00"
        self.file_write.write(cmd.encode('latin-1'))

    def handle_raspi_glitch(self, response):
        """
        @brief Change MSB to 0 for all received characters except the first
        and get a list of characters
        NOTE: having to change the MSB to 0 is a glitch in the raspberry pi,
        and you shouldn't have to do this!
        """
        if self.app_using_python_two():
            return list(map(lambda x: chr(ord(x) & ~0x80), list(response)))
        else:
            return list(map(lambda x: chr(x & ~0x80), list(response)))

    def app_using_python_two(self):
        return sys.version_info[0] < 3

    def get_response(self, raw_data):
        if self.app_using_python_two():
            response = [i for i in raw_data if i != '\x00']
        else:
            response = raw_data

        return response

    def response_valid(self, response):
        valid = True
        error_code = None
        if(len(response) > 0):

            if self.app_using_python_two():
                error_code = str(ord(response[0]))
            else:
                error_code = str(response[0])

            if error_code != '1':  # 1:
                valid = False

        return valid, error_code

    def get_device_info(self):
        """
        @brief get the device info
        @return string moduletype address name
        """
        if(self._name == ""):
            return self._module + " " + str(self.address)
        else:
            return self._module + " " + str(self.address) + " " + self._name

    def read(self, num_of_bytes=31):
        """
        @brief reads a specified number of bytes from I2C,
        then parses and displays the result
        """
        raw_data = self.file_read.read(num_of_bytes)
        response = self.get_response(raw_data=raw_data)
        # print(response)
        is_valid, error_code = self.response_valid(response=response)

        if is_valid:
            char_list = self.handle_raspi_glitch(response[1:])
            # result = "Success " + self.get_device_info()
            # + ": "
            # + str(''.join(char_list))
            # result = "Success: " +  str(''.join(char_list))
            result = "Success %s: %s" % (
                self.get_device_info(),
                str(''.join(char_list))
            )
        else:
            result = "Error " + self.get_device_info() + ": " + error_code

        return result

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
                self.set_i2c_address(i)
                self.read(1)
                i2c_devices.append(i)
            except IOError:
                pass
        # restore the address we were using
        self.set_i2c_address(prev_addr)

        return i2c_devices


class CommonsI2c:
    """ Getters commons methods
    """
    def get_device_info(self, device):
        """
        @brief Get device information
        @param device = AltasI2c instance
        @return device name, firmware version
        """
        return device.query("i")

    def get_read(self, device):
        """
        @brief Read sensor value
        @param device = AltasI2c instance
        @return string (depending of O parameter)
        """
        return device.query("R")

    def get_temperature(self, device):
        """
        @brief Get current compensation temperature
        @param device = AltasI2c instance
        @return string ?T,<temperature value>
        """
        return device.query("T,?")

    def get_calibration(self, device):
        """
        @brief Get current calibrations data
        @param device = AltasI2c instance
        @return ?CAL,<current calibration>
        """
        return device.query("Cal,?")

    def get_find(self, device):
        """
        @brief Fin devices
        @param device = AltasI2c instance
        @return OK
        """
        return device.query("Find")

    def get_status(self, device):
        """
        @brief Get status
        @param device = AltasI2c instance
        @return status of device decode them by using AtlasI2c.AS_RESTART_CODES
        """
        return device.query("Status")

    def get_led(self, device):
        """
        @brief Get led state
        @param device = AltasI2c instance
        @return string ?L,1 for On / ?L,0 for Off
        """
        return device.query("L,?")

    def get_plock(self, device):
        """
        @brief Get Plock status
        @param device = AltasI2c instance
        @return string ?Plock,1 for Locked / ?L,0 for Unlocked
        """
        return device.query("Plock,?")

    """ Setters commons methods
    """
    def set_temperature(self, device, t=25.0):
        """
        @brief Set the compensation temperature
        @param device = AltasI2c instance
        @param t = float temperature value
        """
        return device.query("T,%.2f" % t)

    def set_calibration_low(self, device, solution=0.0):
        """
        @brief calibration 2 points low point
        @param device = AltasI2c instance
        @param float = low solution calibration
        """
        return device.query("Cal,low,%.2f" % solution)

    def set_calibration_high(self, device, solution=0.0):
        """
        @brief calibration 2 points high point
        @param device = AltasI2c instance
        @param float = high solution calibration
        """
        return device.query("Cal,high,%.2f" % solution)

    def set_calibration_clear(self, device):
        """
        @brief Clear calibration data
        @param device = AltasI2c instance
        """
        return device.query("Cal,clear")

    def set_i2c_addr(self, device, add):
        """
        @brief Change the device i2c address
        @param device = AltasI2c instance
        @param int = new i2c add
        """
        if not isinstance(add, int):
            return "only decimal address expected, convert hexa by using \
                AtlasI2c.AS_SENSORS_ADDS_HEXA_TO_DECIMAL"
        else:
            if add not in AtlasI2c.AS_SENSORS_ADDS_DECIMAL:
                return "cannot use this i2c address %d check \
                    AtlasI2c.AS_SENSORS_ADDS_DECIMAL" % add
            else:
                return device.query("I2C,%d" % add)

    def set_led(self, device, state=1):
        """
        @brief Change Led state
        @param device = AltasI2c instance
        @param int or bool state = 1 = On / state = 0 = Off
        """
        return device.query("L,%d" % state)

    def set_sleep_mode(self, device):
        """
        @brief Enter sleep mode / low power
        @param device = AltasI2c instance
        """
        return device.query("Sleep")

    def set_facory(self, device):
        """
        @brief Factory reset, clears calibration, LED on,
        Response codes enabled
        @param device = AltasI2c instance
        """
        return device.query("Factory")

    def set_plock(self, device, state):
        """
        @brief Plock is used to lock the changes between I2C and UART
        @param device = AltasI2c instance
        @param int or bool state = 1 = Locked / state = 0 = Unlocked
        """
        return device.query("Plock, %d" % state)


class ECI2c:
    """
    @brief specific methods for EZO EC module
    """
    """ Getters EC methods
    """
    def get_k_probe(self, device):
        """
        @brief Get current ec probe k
        @param AtlasI2c instance
        @return string ?K,<value of k>
        """
        return device.query("K,?")

    def get_ouput_parameters(self, device):
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
        return device.query("O,?")

    """ Setters EC methods
    """
    def set_k_probe(self, device, k):
        """
        @brief Set the ec probe k
        @param AtlasI2c instance
        @param k float the probe k
        """
        return device.query("K,%.2f" % k)

    def set_calibration_dry(self, device):
        """
        @biref Set the calibration of probe in the air
        @param AtlasI2c instance
        """
        return device.query("Cal,dry")

    def set_calibration_one_point(self, device, point):
        """
        @brief One point calibration
        @param AtlasI2c instance
        @param float or int point to calibrate
        """
        return device.query("Cal,%d" % point)

    def set_output_parameter(self, device, param, state):
        """
        @brief define the output string of read method
        @param string EC/TDS/S/SG
        @param state int or bool 1 = enable / 0 = disable
        """
        return device.query("O,%s,%d" % (param, state,))


class PHI2c:
    """
    @brief specific methods for EZO PH module
    """
    """ Getters pH methods
    """
    def get_slope_probe(self, device):
        """
        @brief Get the pH probe slope
        @param AtlasI2c instance
        @return string ?Slope,<acid closely percent of ideal probe>,
        <base closely percent of ideal probe>,
        <millivolts the zero point is off from true 0>
        """
        return device.query("Slope,?")

    """ Setters pH methods
    """
    def set_calibration_mid(self, device, solution=7.00):
        """
        @brief Calibration the middle point
        @param AtlasI2c instance
        @param float solution value
        """
        return device.query("Cal,mid,%.2f" % solution)