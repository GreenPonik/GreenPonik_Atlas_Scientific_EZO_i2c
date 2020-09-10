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

    def __init__(self, bus=DEFAULT_BUS, addr=None, moduletype=""):
        """
        @brief create instance of AtlasI2c class
        @param int => bus i2c bus number
        @param int/hexa => device i2c address
        @param string => device module type
        """
        if None is addr or (
            addr not in self.ADDR_EZO_HEXA
            and addr not in self.ADDR_EZO_DECIMAL
            and addr not in self.ADDR_OEM_HEXA
            and addr not in self.ADDR_OEM_DECIMAL
        ):
            raise Exception(
                "You have to give a value to addr argument \
                take a look on AtlasI2c.ADDR_EZO_HEXA, \
                AtlasI2c.ADDR_EZO_DECIMAL, \
                AtlasI2c.ADDR_OEM_HEXA \
                and AtlasI2c.ADDR_OEM_DECIMAL"
            )

        if moduletype not in self.ALLOWED_MODULES_TYPES:
            raise Exception(
                "sorry i can just interact \
                with EC or PH moduletype"
            )

        # private properties
        self._debug = False
        self._bus_number = bus
        self._address = addr
        self._name = moduletype.upper()
        self._module = moduletype.upper()
        self._short_timeout = self.SHORT_TIMEOUT
        self._long_timeout = self.LONG_TIMEOUT
        self._smbus = smbus.SMBus(self._bus_number)

    def read(self, register, num_of_bytes=1):
        if num_of_bytes > 1:
            r = self._smbus.read_i2c_block_data(self._address, register, num_of_bytes)
        else:
            r = self._smbus.read_byte_data(self._address, register)

        if self._debug:
            print(r)
        return r

    def write(self, register, values):
        """
        @brief
        """
        if len(values) > 1:
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
    """
    @brief commons methods for EC and PH OEM circuits
    """

    def __init__(self, device):
        self._device = device

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

    def _check_calibration_confirm(self, confirm):
        if self._device.debug:
            if 0x00 == confirm:
                print("Calibration applied")
            else:
                raise Exception("Cannot confirm the operation was correctly executed")

    # ----- Getters ----- ########

    def get_device_info(self):
        """
        @brief Get device information
        @return string module type, firmware version
        """
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
            print(
                "%s: %s%s"
                % (
                    self._device.moduletype,
                    value,
                    "µs" if "EC" == self._device.moduletype else "",
                )
            )
        return value

    def get_temperature(self):
        """
        @brief Get current compensation temperature
        @return float temperature value
        """
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
            print("%s Compensend Temperature: %s°c" % (self._device.moduletype, value))
        return value

    def get_calibration(self):
        """
        @brief Get current calibrations data
        @return string with current points calibrated
        """
        if "EC" == self._device.moduletype:
            register = self._device.OEM_EC_REGISTERS["device_temperature_comp_msb"]
            """bits = {
                "dry": 0,
                "single": 1,
                "low": 2,
                "high": 3,
            }"""
            binary_calib_status = {
                0: "nothing",
                1: "only dry",
                2: "only single",
                3: "dry and single",
                4: "only low",
                5: "dry and low",
                6: "single and low",
                7: "dry, single and low",
                8: "only high",
                9: "dry and high",
                10: "single and high",
                11: "dry, single and high",
                12: "low and high",
                13: "dry, low and high",
                14: "single, low and high",
                15: "all",
            }
        elif "PH" == self._device.moduletype:
            register = self._device.OEM_PH_REGISTERS["device_temperature_comp_msb"]
            """bits = {
                "low": 1,
                "mid": 2,
                "high": 3,
            }"""
            binary_calib_status = {
                0: "nothing",
                1: "only low",
                2: "only mid",
                3: "low and mid",
                4: "only high",
                5: "low and high",
                6: "mid and high",
                7: "all",
            }
        r = self._device.read(register)
        if self._device.debug:
            print("Binary result from OEM", r)
            print("Who is calibrated? >", binary_calib_status[r])
        return binary_calib_status[r]

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
        # define start register address
        if "EC" == self._device.moduletype:
            start_register = self._device.OEM_EC_REGISTERS[
                "device_temperature_comp_msb"
            ]
        elif "PH" == self._device.moduletype:
            start_register = self._device.OEM_PH_REGISTERS[
                "device_temperature_comp_msb"
            ]
        byte_array = int(round(t * 100)).to_bytes(4, "big")
        values = ["0x%02x" % b for b in byte_array]
        self._device.write(start_register, values)
        if self._device.debug:
            print("Temperature to send: %.2f" % t)
            print(
                "%s sent converted temp to bytes: " % (self._device.moduletype),
                values,
            )

    def _set_calibration_registers(self, value):
        """
        @brief calibration value
        in micro µs for EC
        nothing sepcific for pH
        """
        if "EC" == self._device.moduletype:
            start_register = (self._device.OEM_EC_REGISTERS["device_calibration_msb"],)
            byte_array = int(round(value * 100)).to_bytes(4, "big")
            values = ["0x%02x" % b for b in byte_array]
        elif "PH" == self._device.moduletype:
            start_register = self._device.OEM_PH_REGISTERS["device_calibration_msb"]
            byte_array = int(round(value * 1000)).to_bytes(4, "big")
            values = ["0x%02x" % b for b in byte_array]
        self._device.write(start_register, values)
        if self._device.debug:
            print("Value to send: %.2f" % value)
            print(
                "%s sent converted value to bytes: " % (self._device.moduletype),
                values,
            )

    def set_calibration_apply(self, value, point=""):
        """
        @brief apply the calibration
        @param float value => solution calibration
        @param string point => "dry", "single", "low", "mid", "high" only
        """
        if point not in ("dry", "single", "low", "mid", "high"):
            raise Exception('missing string point argument, \
                can only be "dry", "single", "low", "mid", "high"')
        if "EC" == self._device.moduletype:
            points = {"dry": 0x02, "single": 0x03, "low": 0x04, "high": 0x05}
            register = self._device.OEM_EC_REGISTERS["device_calibration_request"]
        elif "PH" == self._device.moduletype:
            points = {"low": 0x02, "mid": 0x03, "high": 0x04}
            register = self._device.OEM_PH_REGISTERS["device_calibration_request"]
        self._set_calibration_registers(value)
        time.sleep(self._device.long_timeout)
        self._device.write(
            register, points[point]
        )  # apply point calibration data
        time.sleep(
            self._device.short_timeout
        )  # wait before read register to get confirmation
        conf = self._device.read(register)
        self._check_calibration_confirm(conf)
        return conf

    def set_calibration_clear(self):
        """
        @brief Clear calibration data
        """
        if "EC" == self._device.moduletype:
            start_register = (
                self._device.OEM_EC_REGISTERS["device_calibration_request"],
            )
        elif "PH" == self._device.moduletype:
            start_register = (
                self._device.OEM_PH_REGISTERS["device_calibration_request"],
            )
        self._device.write(start_register, 0x01)  # send 0x01 to clear calibration data
        time.sleep(
            self._device.short_timeout
        )  # wait before read register to get confirmation
        conf = self._device.read(start_register)
        self._check_calibration_confirm(conf)
        return conf

    def set_i2c_addr(self, addr):
        """
        @brief Change the device i2c address
        @param device = AltasI2c instance
        @param int = new i2c add
        """
        if (
            addr not in self.ADDR_EZO_HEXA
            and addr not in self.ADDR_EZO_DECIMAL
            and addr not in self.ADDR_OEM_HEXA
            and addr not in self.ADDR_OEM_DECIMAL
        ):
            raise Exception(
                "only decimal address expected, convert hexa by using \
                    AtlasI2c.ADDR_OEM_DECIMAL or AtlasI2c.ADDR_EZO_DECIMAL"
            )
        else:
            """
            write workflow to change physical i2c address
            """
            self._device.address(addr)
            raise NotImplementedError("write workflow to change physical i2c address")

    def set_led(self, state=1):
        """
        @brief Change Led state
        @param device = AltasI2c instance
        @param int or bool state = 1 = On / state = 0 = Off
        """
        return self._device.query("L,%d" % state)


class ECI2c(_CommonsI2c):
    """
    @brief specific methods for OEM EC module
    """

    # ----- Getters EC methods ----- ######

    def get_k_probe(self):
        """
        @brief Get current ec probe k
        @param AtlasI2c instance
        @return string ?K,<value of k>
        """
        return self._device.query("K,?")

    # ----- Setters EC methods ----- ######

    def set_k_probe(self, k):
        """
        @brief Set the ec probe k
        @param AtlasI2c instance
        @param k float the probe k
        """
        return self._device.query("K,%.2f" % k)


class PHI2c(_CommonsI2c):
    """
    @brief specific methods for OEM PH module
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

