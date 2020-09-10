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
from adafruit_extended_bus import ExtendedI2C as I2C
from Adafruit_PureIO import smbus


class AtlasI2c:

    ALLOWED_MODULES_TYPES = {
        "EC",
        "PH",
    }
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
        97,  # DO
        98,  # ORP
        99,  # PH
        100,  # EC
    }
    """@brief
    Array key=>value for each EZO sensors name i2c hexa addresses
    """
    ADDR_EZO_TXT_TO_HEXA = {
        "DO": 0x61,
        "ORP": 0x62,
        "PH": 0x63,
        "EC": 0x64,
    }
    """@brief
    Array key=>value for each EZO sensors i2c hexa to decimal addresses
    """
    ADDR_EZO_HEXA_TO_DECIMAL = {
        0x61: 97,  # DO
        0x62: 98,  # ORP
        0x63: 99,  # PH
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
        100,  # EC
        101,  # PH
        102,  # ORP
        103,  # DO
    }
    """@brief
    Array key=>value for each OEM sensors name i2c hexa addresses
    """
    ADDR_OEM_TXT_TO_HEXA = {
        "EC": 0x64,
        "PH": 0x65,
        "ORP": 0x66,
        "DO": 0x67,
    }
    """@brief
    Array key=>value for each OEM sensors i2c hexa to decimal addresses
    """
    ADDR_OEM_HEXA_TO_DECIMAL = {
        0x64: 100,  # DO
        0x65: 101,  # ORP
        0x66: 102,  # PH
        0x67: 103,  # EC
    }

    ONE_BYTE_READ = 0x01
    TWO_BYTE_READ = 0x02
    THREE_BYTE_READ = 0x03
    FOUR_BYTE_READ = 0x04

    OEM_EC_REGISTERS = {
        "device_type": 0x00,
        "device_firmware": 0x01,
        "device_addr_lock": 0x02,
        "device_addr": 0x03,
        "device_intr": 0x04,
        "device_led": 0x05,
        "device_sleep": 0x06,
        "device_new_reading": 0x07,
        "device_probe_type_msb": 0x08,  # 0x08 - 0x09 2 registers
        "device_probe_type_lsb": 0x09,  # 0x08 - 0x09 2 registers
        "device_calibration_value_msb": 0x0A,  # 0x0A - 0x0D 4 registers
        "device_calibration_value_high": 0x0B,  # 0x0A - 0x0D 4 registers
        "device_calibration_value_low": 0x0C,  # 0x0A - 0x0D 4 registers
        "device_calibration_value_lsb": 0x0D,  # 0x0A - 0x0D 4 registers
        "device_calibration_request": 0x0E,
        "device_calibration_confirm": 0x0F,
        "device_temperature_comp_msb": 0x10,  # 0x10 - 0x13 4 registers
        "device_temperature_comp_high": 0x11,  # 0x10 - 0x13 4 registers
        "device_temperature_comp_low": 0x12,  # 0x10 - 0x13 4 registers
        "device_temperature_comp_lsb": 0x13,  # 0x10 - 0x13 4 registers
        "device_temperature_confirm_msb": 0x14,  # 0x14 - 0x17 4 registers
        "device_temperature_confirm_high": 0x15,  # 0x14 - 0x17 4 registers
        "device_temperature_confirm_low": 0x16,  # 0x14 - 0x17 4 registers
        "device_temperature_confirm_lsb": 0x17,  # 0x14 - 0x17 4 registers
        "device_ec_msb": 0x18,  # 0x18 - 0x1B 4 registers
        "device_ec_high": 0x19,  # 0x18 - 0x1B 4 registers
        "device_ec_low": 0x20,  # 0x18 - 0x1B 4 registers
        "device_ec_lsb": 0x21,  # 0x18 - 0x1B 4 registers
        "device_tds_msb": 0x1C,  # 0x1C - 0x1F 3 registers
        "device_tds_high": 0x1D,  # 0x1C - 0x1F 3 registers
        "device_tds_low": 0x1E,  # 0x1C - 0x1F 3 registers
        "device_tds_lsb": 0x1F,  # 0x1C - 0x1F 3 registers
        "device_salinity_msb": 0x20,  # 0x20 - 0x23 4 registers
        "device_salinity_high": 0x21,  # 0x20 - 0x23 4 registers
        "device_salinity_low": 0x22,  # 0x20 - 0x23 4 registers
        "device_salinity_lsb": 0x23,  # 0x20 - 0x23 4 registers
    }

    OEM_PH_REGISTERS = {
        "device_type": 0x00,
        "device_firmware": 0x01,
        "device_addr_lock": 0x02,
        "device_addr": 0x03,
        "device_intr": 0x04,
        "device_led": 0x05,
        "device_sleep": 0x06,
        "device_new_reading": 0x07,
        "device_calibration_msb": 0x08,  # 0x08 - 0x0B 4 registers
        "device_calibration_high": 0x09,  # 0x08 - 0x0B 4 registers
        "device_calibration_low": 0x0A,  # 0x08 - 0x0B 4 registers
        "device_calibration_lsb": 0x0B,  # 0x08 - 0x0B 4 registers
        "device_calibration_request": 0x0C,
        "device_calibration_confirm": 0x0D,
        "device_temperature_comp_msb": 0x0E,  # 0x0E - 0x11 4 registers
        "device_temperature_comp_high": 0x0F,  # 0x0E - 0x11 4 registers
        "device_temperature_comp_low": 0x10,  # 0x0E - 0x11 4 registers
        "device_temperature_comp_lsb": 0x11,  # 0x0E - 0x11 4 registers
        "device_temperature_confirm_msb": 0x12,  # 0x12 - 0x15 4 registers
        "device_temperature_confirm_high": 0x13,  # 0x12 - 0x15 4 registers
        "device_temperature_confirm_low": 0x14,  # 0x12 - 0x15 4 registers
        "device_temperature_confirm_lsb": 0x15,  # 0x12 - 0x15 4 registers
        "device_ph_msb": 0x16,  # 0x16 - 0x19 4 registers
        "device_ph_high": 0x17,  # 0x16 - 0x19 4 registers
        "device_ph_low": 0x18,  # 0x16 - 0x19 4 registers
        "device_ph_lsb": 0x19,  # 0x16 - 0x19 4 registers
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
    SHORT_TIMEOUT = 0.3

    LONG_TIMEOUT_COMMANDS = ("R", "CAL")
    SLEEP_COMMANDS = ("SLEEP",)

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, d):
        self._debug = d

    @property
    def bus_number(self):
        return self._bus_number

    @bus_number.setter
    def bus_number(self, bus_number):
        self._bus_number = bus_number

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
    def name(self, name):
        self._name = name

    @property
    def moduletype(self):
        return self._module

    @moduletype.setter
    def moduletype(self, m):
        self._module = m.upper()

    def __init__(self, bus=DEFAULT_BUS, addr=DEFAULT_ADDR, moduletype=""):
        """
        open two file streams, one for reading and one for writing
        the specific I2C channel is selected with bus
        it is usually 1, except for older revisions where its 0
        wb and rb indicate binary read and write
        """
        # private properties
        self._debug = False
        self._bus_number = bus
        self._address = addr
        self._name = moduletype.upper()
        self._module = moduletype.upper()
        self._short_timeout = self.SHORT_TIMEOUT
        self._long_timeout = self.LONG_TIMEOUT
        self._smbus = smbus.SMBus(self._bus_number)

    def get_command_timeout(self, command):
        timeout = None
        if command.upper().startswith(self.LONG_TIMEOUT_COMMANDS):
            timeout = self._long_timeout
        elif not command.upper().startswith(self.SLEEP_COMMANDS):
            timeout = self.short_timeout
        if self._debug:
            print(timeout)
        return timeout

    def query(self, command):
        """
        @brief write a command to the board, wait the correct timeout,
        and read the response
        """
        pass

    def read(self, register, num_of_bytes=1):
        if num_of_bytes > 1:
            r = self._smbus.read_i2c_block_data(
                self._address, register, num_of_bytes
            )
        else:
            r = self._smbus.read_byte_data(self._address, register)

        if self._debug:
            print(r)
        return r

    def write(self, register, values):
        """
        @brief
        """
        if values > 1:
            self._smbus.write_block_data(self._address, register, values)
        else:
            self._smbus.write_byte_data(self._address, register, values)

    def list_i2c_devices(self):
        """
        @brief save the current address so we can restore it after
        """
        with I2C(self._bus_number) as i2c:
            scan = i2c.scan()
            if self._debug:
                print(scan)
            return scan


class _CommonsI2c:

    def __init__(self, device):
        self._device = device

    def _check_module_type(self, moduletype):
        """
        @brief check if instance of AtlasI2C have allowed moduletype
        """
        if moduletype not in self._device.ALLOWED_MODULES_TYPES:
            raise Exception("sorry i can just read device info for EC or PH moduletype")
        else:
            return True

    def _convert_raw_hex_to_float(self, byte_array):
        """
        @brief convert bytearray response to float result
        return float converted value
        """
        hexstr = byte_array.hex()
        float_from_hexa = float.fromhex(byte_array.hex())
        converted = float_from_hexa
        if self._device.debug:
            print("Byte Array to decode: ")
            print(byte_array)
            print("Decoded to hexa string: %s" % hexstr)
        return converted

    # ----- Getters ----- ########

    def get_device_info(self):
        """
        @brief Get device information
        @return string module type, firmware version
        """
        if self._check_module_type(self._device.moduletype):
            if "EC" == self._device.moduletype or "PH" == self._device.moduletype:
                info = self._device.read(
                    self._device.OEM_EC_REGISTERS["device_type"],
                    self._device.TWO_BYTE_READ,
                )
            return "SUCCESS: %s, module type: %s and firmware is: %s" % (
                self._device.moduletype,
                info[0],
                info[1],
            )

    def get_type(self):
        """
        @brief Read sensor type
        @return int the sensor type (1=EC, 4=PH)
        """
        if self._check_module_type(self._device.moduletype):
            if "EC" == self._device.moduletype or "PH" == self._device.moduletype:
                device_type = self._device.read(
                    self._device.OEM_EC_REGISTERS["device_type"],
                    self._device.ONE_BYTE_READ,
                )
            if self._device.debug:
                print("Device type is: %s" % device_type)
            return device_type

    def get_firmware(self):
        """
        @brief Read sensor firmware
        @return int the firmware revision
        """
        if self._check_module_type(self._device.moduletype):
            if "EC" == self._device.moduletype or "PH" == self._device.moduletype:
                firmware = self._device.read(
                    self._device.OEM_EC_REGISTERS["device_firmware"],
                    self._device.ONE_BYTE_READ,
                )
            if self._device.debug:
                print("Firmware type is: %s" % firmware)
            return firmware

    def get_read(self):
        """
        @brief Read sensor value
        @return float the sensor value
        """
        if self._check_module_type(self._device.moduletype):
            if "EC" == self._device.moduletype:
                rawhex = self._device.read(
                    self._device.OEM_EC_REGISTERS["device_ec_msb"],
                    self._device.FOUR_BYTE_READ,
                )
                value = self._convert_raw_hex_to_float(rawhex) / 100
            elif "PH" == self._device.moduletype:
                rawhex = self._device.read(
                    self._device.OEM_PH_REGISTERS["device_ph_msb"],
                    self._device.FOUR_BYTE_READ,
                )
                value = self._convert_raw_hex_to_float(rawhex) / 1000
            if self._device.debug:
                print("%s: %s%s" % (
                    self._device.moduletype,
                    value,
                    "µs" if "EC" == self._device.moduletype else "")
                )
            return value

    def get_temperature(self):
        """
        @brief Get current compensation temperature
        @param device = AltasI2c instance
        @return string ?T,<temperature value>
        """
        if self._check_module_type(self._device.moduletype):
            if "EC" == self._device.moduletype:
                rawhex = self._device.read(
                    self._device.OEM_EC_REGISTERS["device_temperature_confirm_msb"],
                    self._device.FOUR_BYTE_READ,
                )
            elif "PH" == self._device.moduletype:
                rawhex = self._device.read(
                    self._device.OEM_PH_REGISTERS["device_temperature_confirm_msb"],
                    self._device.FOUR_BYTE_READ,
                )
            value = self._convert_raw_hex_to_float(rawhex) / 100
            if self._device.debug:
                print("%s Compensend Temperature: %s°c" % (
                    self._device.moduletype,
                    value)
                )
            return value

    def get_calibration(self):
        """
        @brief Get current calibrations data
        @param device = AltasI2c instance
        @return ?CAL,<current calibration>
        """
        return self._device.query("Cal,?")

    def get_led(self):
        """
        @brief Get led state
        @param device = AltasI2c instance
        @return string ?L,1 for On / ?L,0 for Off
        """
        return self._device.query("L,?")

    # ----- Setters ----- ########

    def set_temperature(self, t=25.0):
        """
        @brief Set the compensation temperature
        @param t = float temperature value
        """
        byte_array = int(round(t * 100)).to_bytes(4, "big")
        values = ["0x%02x" % b for b in byte_array]
        if self._check_module_type(self._device.moduletype):
            if "EC" == self._device.moduletype:
                start_register = self._device.OEM_EC_REGISTERS["device_temperature_comp_msb"],
            elif "PH" == self._device.moduletype:
                start_register = self._device.OEM_PH_REGISTERS["device_temperature_comp_msb"]
            self._device.write(
                start_register,
                values
            )
            if self._device.debug:
                print("Temperature to send: %.2f" % t)
                print("%s sent converted temp to bytes: " % (self._device.moduletype), values)

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
            if (
                add not in AtlasI2c.ADDR_OEM_DECIMAL
                and add not in AtlasI2c.ADDR_EZO_DECIMAL
            ):
                return (
                    "cannot use this i2c address %d check \
                    AtlasI2c.ADDR_OEM_DECIMAL or AtlasI2c.ADDR_EZO_DECIMAL"
                    % add
                )
            else:
                """
                write workflow to change physical i2c address
                """
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
        return self._device.query(
            "O,%s,%d"
            % (
                param,
                state,
            )
        )


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
