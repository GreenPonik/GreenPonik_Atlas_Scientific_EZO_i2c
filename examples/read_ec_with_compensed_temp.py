from src/atlas_zero_i2c import AtlasEzoI2c
from src/ezo_ec import *
from GreenPonik_thermistor_10k import GreenPonik_thermistor_10k

if __name__ == "__main__":
    print("get device infos")
    ezo_ec = AtlasI2C(address=AtlasEzoI2c.AS_SENSORS_ADDS_TXT_TO_DECIMAL['EC'], moduletype="EC", name="EC")
    print(get_device_info(ezo_ec))
    print("get current temperature compensated")
    print(get_temperature(ezo_ec))
    temp = GreenPonik_thermistor_10k.read_temp()
    print(set_temperature(ezo_ec, temp))
    get_read(ezo_ec)