import unittest
from GreenPonik_Atlas_Scientific_i2c.GreenPonik_Atlas_Scientific_i2c import AtlasI2c, CommonsI2c


# TODO implement mock to emulate I2C bus


class TestGreenPonik_altals_Scientifics_I2C(unittest.TestCase):

    def test_get_device_info(self):
        device = AtlasI2c(
            address=AtlasI2c.AS_SENSORS_ADDS_TXT_TO_DECIMAL['EC'], moduletype="EC", name="EC")
        infos = CommonsI2c.get_device_info(device)
        self.assertEqual(infos, "bob")

    def test_get_read(self):
        device = AtlasI2c(
            address=AtlasI2c.AS_SENSORS_ADDS_TXT_TO_DECIMAL['EC'], moduletype="EC", name="EC")
        value = CommonsI2c.get_read(device)
        self.assertEqual(value, "tutu")


if __name__ == '__main__':
    unittest.main()
