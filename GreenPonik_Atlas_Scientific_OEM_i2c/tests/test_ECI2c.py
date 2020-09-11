import unittest
from unittest.mock import patch, MagicMock
import sys


class Test_ECI2c(unittest.TestCase):
    @patch("GreenPonik_Atlas_Scientific_i2c.GreenPonik_ECI2c.ECI2c")
    def test_get_device_info(self, Mock):
        ec_i2c = Mock()
        expected = "SUCCESS: EC, module type: 4 and firmware is: 5"
        ec_i2c.get_device_info.return_value = expected
        info = ec_i2c.get_device_info()
        self.assertIsNotNone(info)
        self.assertEqual(info, expected)

    @patch("GreenPonik_Atlas_Scientific_i2c.GreenPonik_ECI2c.ECI2c")
    def test_get_type(self, Mock):
        ec_i2c = Mock()
        expected = 4
        ec_i2c.get_type.return_value = expected
        value = ec_i2c.get_type()
        self.assertIsNotNone(value)
        self.assertTrue(type(value).__name__, "int")
        self.assertEqual(value, expected)

    @patch("GreenPonik_Atlas_Scientific_i2c.GreenPonik_ECI2c.ECI2c")
    def test_get_firmware(self, Mock):
        ec_i2c = Mock()
        expected = 5
        ec_i2c.get_firmware.return_value = expected
        value = ec_i2c.get_firmware()
        self.assertIsNotNone(value)
        self.assertTrue(type(value).__name__, "int")
        self.assertEqual(value, expected)

    @patch("GreenPonik_Atlas_Scientific_i2c.GreenPonik_ECI2c.ECI2c")
    def test_get_read(self, Mock):
        ec_i2c = Mock()
        expected = 24.56
        ec_i2c.get_read.return_value = expected
        value = ec_i2c.get_read()
        self.assertIsNotNone(value)
        self.assertTrue(type(value).__name__, "float")
        self.assertEqual(value, expected)


if __name__ == '__main__':
    unittest.main()
