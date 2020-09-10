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


class _CommonsI2c:
    """
    @brief commons methods for EC and PH OEM circuits
    """

    def __init__(self, device):
        """
        @brief pass has argument an instance of AtlasI2C class
        """
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
        if self._device.debug:
            print("Temperature to send: %.2f" % t)
            print(
                "%s sent converted temp to bytes: " % (self._device.moduletype),
                values,
            )
        self._device.write(start_register, values)

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
