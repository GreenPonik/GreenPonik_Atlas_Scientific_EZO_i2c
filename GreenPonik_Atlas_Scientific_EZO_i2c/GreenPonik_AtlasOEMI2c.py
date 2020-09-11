#! /usr/bin/python3
"""
@package Class to communicate with Atlas Scientific OEM sensors in I2C mode.
#######################################################################
#######################################################################
#######################################################################
##################### Atlas Scientific i2c ############################
######################### by GreenPonik ###############################
#######################################################################
#######################################################################
#######################################################################
Source code is based on Atlas Scientific documentations:
https://www.atlas-scientific.com/files/EC_oem_datasheet.pdf
https://atlas-scientific.com/files/oem_pH_datasheet.pdf
"""
import time
from adafruit_extended_bus import ExtendedI2C as I2C
from Adafruit_PureIO.smbus import SMBus


class _AtlasOEMI2c:

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
    def mysmbus(self):
        return self._smbus

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
        self._smbus = SMBus(self._bus_number)

    def read(self, register, num_of_bytes=1):
        """
        @brief
        """
        if num_of_bytes > 1:
            raw = self._smbus.read_i2c_block_data(self._address, register, num_of_bytes)
        else:
            raw = self._smbus.read_byte_data(self._address, register)

        if self._debug:
            print("Read: %s registers start from: %s" % (num_of_bytes, hex(register)))
            print("Raw response from i2c: ", raw)
        return raw

    def _prepare_values_to_write_block(self, v):
        """
        @brief from AdafruitPureIO smbus class
        the write_block_data(self, addr, cmd, vals) need specific data organisation to work:
        >>  `Write a block of data to the specified cmd register of the device.
            The amount of data to write should be the first byte inside the vals
            string/bytearray and that count of bytes of data to write should follow it.`
        """
        b = bytearray(len(v) + 1)
        b[0] = len(v)
        i = 1
        for elm in v:
            b[i] = hex(elm)
            i += 1
        return b

    def write(self, register, v):
        """
        @brief
        """
        if("int" != type(v).__name__
           and len(v) > 1
           and ("bytearray" == type(v).__name__ or "bytes" == type(v).__name__)
           ):
            # v = self._prepare_values_to_write_block(v)
            # self._smbus.write_block_data(self._address, register, v)
            self.mysmbus.write_i2c_block_data(self._address, register, v)
        elif "int" == type(v).__name__:
            self.mysmbus.write_byte_data(self._address, register, v)
        else:  # "str" == type(v).__name__:
            raise Exception("cannot write this in smbus/i2c: ", v)
        if self._debug:
            print("Write %s on register: %s" % (v, hex(register)))

    def list_i2c_devices(self):
        """
        @brief save the current address so we can restore it after
        """
        with I2C(self._bus_number) as i2c:
            scan = i2c.scan()
            if self._debug:
                print("I2c devices found: ", scan)
            return scan

    def print_all_registers_values(self):
        if "EC" == self._module:
            registers = self.OEM_EC_REGISTERS
        elif "PH" == self._module:
            registers = self.OEM_PH_REGISTERS
        for reg in range(0, len(registers)):
            print("Register: %s, Value: %s" % (hex(reg), self.read(reg)))
