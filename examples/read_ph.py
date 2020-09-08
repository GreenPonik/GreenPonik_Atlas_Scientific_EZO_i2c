from GreenPonik_Altas_Scientific_i2c.GreenPonik_Altas_Scientific_i2c import AtlasI2c, CommonsI2c, PHI2c

if __name__ == "__main__":
    try:
        print("get device infos")
        ph_i2c = AtlasI2c(
            address=AtlasI2c.AS_SENSORS_ADDS_TXT_TO_DECIMAL['PH'],
            moduletype="PH",
            name="PH"
        )
        c = CommonsI2c()
        print(c.get_device_info(ph_i2c))
        print(c.get_read(ph_i2c))
    except Exception as e:
        print("Exception occured", e)
