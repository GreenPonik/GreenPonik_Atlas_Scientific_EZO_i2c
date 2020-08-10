from GreenPonik_Altas_Scientific_i2c import AtlasI2c, CommonsI2c, PHI2c

if __name__ == "__main__":
    print("get device infos")
    ph_i2c = AtlasI2c(address=AtlasI2c.AS_SENSORS_ADDS_TXT_TO_DECIMAL['PH'], moduletype="PH", name="PH")
    print(CommonsI2c.get_device_info(ph_i2c))
    print(CommonsI2c.get_read(ph_i2c))