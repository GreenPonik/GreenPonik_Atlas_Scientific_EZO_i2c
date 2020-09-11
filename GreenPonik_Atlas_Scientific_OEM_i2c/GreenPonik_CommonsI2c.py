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

import time
from GreenPonik_Atlas_Scientific_i2c.GreenPonik_AtlasOEMI2c import _AtlasOEMI2c


class _CommonsI2c(_AtlasOEMI2c):
    """
    @brief commons methods for EC and PH OEM circuits
    """

    # def __init__(self, device: AtlasI2c):
    #     """
    #     @brief pass has argument an instance of AtlasI2C class
    #     """
    #     self = device

    def _convert_raw_hex_to_float(self, byte_array):
        """
        @brief convert bytearray response to float result
        return float converted value
        """
        hexstr = byte_array.hex()
        float_from_hexa = float.fromhex(byte_array.hex())
        converted = float_from_hexa
        if self.debug:
            print("Byte Array to decode: ", byte_array)
            print("Byte Array decoded to hexa string: %s" % hexstr)
        return converted

    def _check_calibration_confirm(self, confirm):
        """
        @brief check the response of calibration confirm register
        """
        if self.debug:
            if hex(0x00) == hex(confirm):
                print("Calibration applied")
            else:
                raise Exception("Cannot confirm the operation was correctly executed")

    # ----- Getters ----- ########

    def get_device_info(self):
        """
        @brief Get device information
        @return string module type, firmware version
        """
        if "EC" == self.moduletype or "PH" == self.moduletype:
            info = self.read(
                self.OEM_EC_REGISTERS["device_type"],
                self.TWO_BYTE_READ,
            )
        return "SUCCESS: %s, module type: %s and firmware is: %s" % (
            self.moduletype,
            info[0],
            info[1],
        )

    def get_type(self):
        """
        @brief Read sensor type
        @return int the sensor type (1=EC, 4=PH)
        """
        if "EC" == self.moduletype or "PH" == self.moduletype:
            device_type = self.read(
                self.OEM_EC_REGISTERS["device_type"],
                self.ONE_BYTE_READ,
            )
        if self.debug:
            print("Device type is: %s" % device_type)
        return device_type

    def get_firmware(self):
        """
        @brief Read sensor firmware
        @return int the firmware revision
        """
        if "EC" == self.moduletype or "PH" == self.moduletype:
            firmware = self.read(
                self.OEM_EC_REGISTERS["device_firmware"],
                self.ONE_BYTE_READ,
            )
        if self.debug:
            print("Firmware type is: %s" % firmware)
        return firmware

    def get_read(self):
        """
        @brief Read sensor value
        @return float the sensor value
        """
        self.set_wakeup_sleep_mode(0x01)  # wake device before read
        if "EC" == self.moduletype:
            rawhex = self.read(
                self.OEM_EC_REGISTERS["device_ec_msb"],
                self.FOUR_BYTE_READ,
            )
            value = self._convert_raw_hex_to_float(rawhex) / 100
        elif "PH" == self.moduletype:
            rawhex = self.read(
                self.OEM_PH_REGISTERS["device_ph_msb"],
                self.FOUR_BYTE_READ,
            )
            value = self._convert_raw_hex_to_float(rawhex) / 1000
        if self.debug:
            print(
                "%s: %s%s"
                % (
                    self.moduletype,
                    value,
                    "µs" if "EC" == self.moduletype else "",
                )
            )
        self.set_wakeup_sleep_mode(0x00)  # sleep device after read
        return value

    def get_temperature(self):
        """
        @brief Get current compensation temperature
        @return float temperature value
        """
        if "EC" == self.moduletype:
            rawhex = self.read(
                self.OEM_EC_REGISTERS["device_temperature_comp_msb"],
                self.FOUR_BYTE_READ,
            )
        elif "PH" == self.moduletype:
            rawhex = self.read(
                self.OEM_PH_REGISTERS["device_temperature_comp_msb"],
                self.FOUR_BYTE_READ,
            )
        value = self._convert_raw_hex_to_float(rawhex) / 100
        if self.debug:
            print("%s Compensend Temperature: %s°c" % (self.moduletype, value))
        return value

    def get_calibration(self):
        """
        @brief Get current calibrations data
        @return string with current points calibrated
        """
        if "EC" == self.moduletype:
            register = self.OEM_EC_REGISTERS["device_calibration_confirm"]
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
        elif "PH" == self.moduletype:
            register = self.OEM_PH_REGISTERS["device_calibration_confirm"]
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
        r = self.read(register)
        if self.debug:
            print("Binary result from OEM", r)
            print("Who is calibrated? >", binary_calib_status[r])
        return binary_calib_status[r]

    def get_led(self):
        """
        @brief Get led state
        register is the same for EC and PH OEM circuit
        @return byte/int 0x00/0 = OFF / 0x01/1 = ON
        """
        register = self.OEM_EC_REGISTERS["device_led"]
        led_status = self.read(register)
        if self.debug:
            print("Led status is currently:  %s" % hex(led_status))
        return led_status

    def get_wakeup_sleep_mode(self):
        """
        @brief get Active or Hibernate device mode
        register is the same for EC and PH OEM circuit
        @return byte/int 0x01/1 = WakeUp / 0x00/0 = Hibernate
        """
        register = self.OEM_EC_REGISTERS["device_sleep"]
        mode = self.read(register)
        if self.debug:
            print("Device is currently in mode:  %s" % ("wakeup" if 0x01 == hex(mode) else "sleep"))

    # ----- Setters ----- ########

    def set_temperature(self, t=25.0):
        """
        @brief Set the compensation temperature
        @param t = float temperature value
        """
        if "EC" == self.moduletype:
            start_register = self.OEM_EC_REGISTERS[
                "device_temperature_comp_msb"
            ]
        elif "PH" == self.moduletype:
            start_register = self.OEM_PH_REGISTERS[
                "device_temperature_comp_msb"
            ]
        byte_array = int(round(t * 100)).to_bytes(4, "big")
        # values = ["0x%02x" % b for b in byte_array]
        if self.debug:
            print("Temperature to set: %.2f" % t)
            print(
                "%s sent converted temp to bytes: " % (self.moduletype),
                byte_array,
            )
        time.sleep(self.short_timeout)
        self.write(start_register, byte_array)

    def _set_calibration_registers(self, value):
        """
        @brief calibration registers
        do not use alone because calibration is apply by using set_calibration_apply
        /!in micro µs for EC nothing sepcific for pH/!
        """
        if "EC" == self.moduletype:
            start_register = (self.OEM_EC_REGISTERS["device_calibration_msb"],)
            byte_array = int(round(value * 100)).to_bytes(4, "big")
            # values = ["0x%02x" % b for b in byte_array]
        elif "PH" == self.moduletype:
            start_register = self.OEM_PH_REGISTERS["device_calibration_msb"]
            byte_array = int(round(value * 1000)).to_bytes(4, "big")
            # values = ["0x%02x" % b for b in byte_array]
        self.write(start_register, byte_array)
        if self.debug:
            print("Value to send: %.2f" % value)
            print(
                "%s sent converted value to bytes: " % (self.moduletype),
                byte_array,
            )

    def set_calibration_apply(self, value, point=""):
        """
        @brief apply the calibration
        @param float value => solution calibration value e.g. 4.02
        @param string point => "dry", "single", "low", "mid", "high" only
        """
        if point not in ("dry", "single", "low", "mid", "high"):
            raise Exception('missing string point argument, \
                can only be "dry", "single", "low", "mid", "high"')
        if "EC" == self.moduletype:
            points = {"dry": 0x02, "single": 0x03, "low": 0x04, "high": 0x05}
            register = self.OEM_EC_REGISTERS["device_calibration_request"]
        elif "PH" == self.moduletype:
            points = {"low": 0x02, "mid": 0x03, "high": 0x04}
            register = self.OEM_PH_REGISTERS["device_calibration_request"]
        self._set_calibration_registers(value)
        time.sleep(self.long_timeout)
        self.write(
            register, points[point]
        )  # apply point calibration data
        time.sleep(
            self.short_timeout
        )  # wait before read register to get confirmation
        conf = self.read(register)
        self._check_calibration_confirm(conf)
        return conf

    def set_calibration_clear(self):
        """
        @brief Clear calibration data
        """
        if "EC" == self.moduletype:
            register = (
                self.OEM_EC_REGISTERS["device_calibration_request"],
            )
        elif "PH" == self.moduletype:
            register = (
                self.OEM_PH_REGISTERS["device_calibration_request"],
            )
        self.write(register, 0x01)  # send 0x01 to clear calibration data
        time.sleep(
            self.short_timeout
        )  # wait before read register to get confirmation
        conf = self.read(register)
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
            self.address(addr)
            raise NotImplementedError("write workflow to change physical i2c address")

    def set_led(self, state=0x01):
        """
        @brief Change Led state
        @param byte/int state => 0x01/1 = On / 0x00/0 = Off
        """
        register = self.OEM_EC_REGISTERS["device_led"]
        self.write(register, state)
        if self.debug:
            print("Led status change to:  %s" % ("On" if hex(0x01) == hex(state) else "OFF"))

    def set_wakeup_sleep_mode(self, action=0x01):
        """
        @brief change device mode to Active or Hibernate
        register is the same for EC and PH OEM circuit
        @param byte/int action => 0x01/1 = WakeUp / 0x00/0 = Hibernate
        """
        register = self.OEM_EC_REGISTERS["device_sleep"]
        self.write(register, action)
        if self.debug:
            print("Device is now:  %s" % ("wakeup" if hex(0x01) == hex(action) else "sleep"))
