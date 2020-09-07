import unittest
from unittest.mock import patch, MagicMock
import sys


class FCNTLMock:
    def __init__(self):
        pass


class BoardMock:
    def __init__(self):
        self._scl = 18
        self._sda = 15

    def SCL(self):
        return self._scl

    def SDA(self):
        return self._sda


class BusioMock(MagicMock()):
    def I2C(self, sda, scl):
        return True


sys.modules["fcntl"] = FCNTLMock
sys.modules["board"] = BoardMock()
sys.modules["busio"] = BusioMock()


from GreenPonik_Atlas_Scientific_i2c.GreenPonik_Atlas_Scientific_i2c import (
    AtlasI2c,
    CommonsI2c
)


class Test_GreenPonik_Altals_Scientifics_i2c(unittest.TestCase):
    @patch("GreenPonik_Atlas_Scientific_i2c.GreenPonik_Atlas_Scientific_i2c.CommonsI2c")
    def test_get_device_info(self, Mock):
        device = AtlasI2c()
        common = Mock()
        expected = 0x64
        common.get_device_info.return_value = expected
        common.set_i2c_addr(
            device, AtlasI2c.AS_SENSORS_ADDS_TXT_TO_DECIMAL['EC'])
        addr = common.get_device_info(device)
        self.assertIsNotNone(addr)
        self.assertEqual(addr, expected)

    @patch("GreenPonik_Atlas_Scientific_i2c.GreenPonik_Atlas_Scientific_i2c.CommonsI2c")
    def test_get_read(self, Mock):
        device = AtlasI2c()
        common = Mock()
        expected = 24.56
        common.get_read.return_value = expected
        common.set_i2c_addr(
            device, AtlasI2c.AS_SENSORS_ADDS_TXT_TO_DECIMAL['EC'])
        value = common.get_read(device)
        self.assertIsNotNone(value)
        self.assertTrue(type(value).__name__, "float")
        self.assertEqual(value, expected)


if __name__ == '__main__':
    unittest.main()
