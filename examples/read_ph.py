from GreenPonik_Altas_Scientific_i2c.GreenPonik_Altas_Scientific_i2c import AtlasI2c, PHI2c

if __name__ == "__main__":
    try:
        print("get device infos")
        i2c_device = AtlasI2c(
            address=AtlasI2c.ADDR_EZO_TXT_TO_HEXA['PH'],
            moduletype="PH",
            name="PH"
        )
        ph_i2c = PHI2c(i2c_device)
        print(ph_i2c.get_device_info())
        print(ph_i2c.get_read())
    except Exception as e:
        print("Exception occured", e)