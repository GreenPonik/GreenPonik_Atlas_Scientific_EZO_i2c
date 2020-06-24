from GreenPonik_Atlas_Scientific_i2c.GreenPonik_Atlas_Scientific_i2c import AtlasI2c
from GreenPonik_Atlas_Scientific_i2c.ec_i2c import *
from GreenPonik_thermistor_10k import GreenPonik_thermistor_10k

if __name__ == "__main__":
    print("get device infos")
    ec_i2c = AtlasI2C(address=AtlasI2c.AS_SENSORS_ADDS_TXT_TO_DECIMAL['EC'], moduletype="EC", name="EC")
    print(get_device_info(ec_i2c))
    print("get current temperature compensated")
    print(get_temperature(ec_i2c))
    t = GreenPonik_thermistor_10k.read_temp()
    print(set_temperature(ec_i2c, t))
    get_read(ec_i2c)