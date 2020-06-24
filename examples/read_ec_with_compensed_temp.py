from GreenPonik_Atlas_Scientific_i2c import AtlasI2c
import commons_i2c
from GreenPonik_thermistor_10k import GreenPonik_thermistor_10k

if __name__ == "__main__":
    print("get device infos")
    ec_i2c = AtlasI2c(address=AtlasI2c.AS_SENSORS_ADDS_TXT_TO_DECIMAL['EC'], moduletype="EC", name="EC")
    print(commons_i2c.get_device_info(ec_i2c))
    print("get current temperature compensated")
    print(commons_i2c.get_temperature(ec_i2c))
    t = GreenPonik_thermistor_10k.read_temp()
    print(commons_i2c.set_temperature(ec_i2c, t))
    ec = commons_i2c.get_read(ec_i2c)
    print("current ec is %.2f" % ec)