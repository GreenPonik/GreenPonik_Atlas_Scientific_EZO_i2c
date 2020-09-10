import unittest
from unittest.mock import patch, MagicMock
import sys


class FNCTLMock():
    def __init__(self):
        pass

    def ioctl():
        pass


class SmbusMock:
    def __init__(self):
        pass


# sys.modules["ioctl"] = IOCTLMock()
sys.modules["fcntl"] = FNCTLMock()
sys.modules["smbus"] = SmbusMock()

from GreenPonik_Atlas_Scientific_i2c.GreenPonik_AtlasI2c import AtlasI2c


class Test_GreenPonik_AtlasI2c(unittest.TestCase):
    @patch("GreenPonik_Atlas_Scientific_i2c.GreenPonik_AtlasI2c.AtlasI2c")
    def test_list_i2c_devices(self, Mock):
        i2c_device = Mock()
        expected = [0x64, 0x65]
        i2c_device.list_i2c_devices.return_value = expected
        devices = i2c_device.list_i2c_devices()
        self.assertIsNotNone(devices)
        self.assertEqual(devices, expected)


if __name__ == '__main__':
    unittest.main()
