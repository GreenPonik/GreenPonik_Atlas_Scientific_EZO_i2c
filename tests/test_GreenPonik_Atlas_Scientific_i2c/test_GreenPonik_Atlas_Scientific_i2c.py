import sys
import unittest
from GreenPonik_Atlas_Scientific_i2c import AtlasI2c
from GreenPonik_Atlas_Scientific_i2c import commons_i2c

try:
    import unittest.mock as mock
except ImportError:
    import mock


# import ec_i2c
# import ph_i2c

#TODO implement mock to emulate I2C bus

# Test cases
class TestGreenPonik_altals_Scientifics_I2C(unittest.TestCase):
    
    def test_get_device_info(self):
        device = AtlasI2c(address=AtlasI2c.AS_SENSORS_ADDS_TXT_TO_DECIMAL['EC'], moduletype="EC", name="EC")
        infos = commons_i2c.get_device_info(device)
        self.assertEqual(infos, "bob")
    
    def test_get_read(self):
        device = AtlasI2c(address=AtlasI2c.AS_SENSORS_ADDS_TXT_TO_DECIMAL['EC'], moduletype="EC", name="EC")
        value = commons_i2c.get_read(device)
        self.assertEqual(value, "tutu")

if __name__ == '__main__':
    unittest.main()