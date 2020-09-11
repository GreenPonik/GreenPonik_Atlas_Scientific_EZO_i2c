from GreenPonik_Altas_Scientific_OEM_i2c.GreenPonik_PHI2c import PHI2c

if __name__ == "__main__":
    try:
        print("get device infos")
        ph_i2c = PHI2c(
            bus=1,
            address=PHI2c.ADDR_EZO_TXT_TO_HEXA['PH'],
            moduletype="PH",
            name="PH"
        )
        print(ph_i2c.get_device_info())
        print(ph_i2c.get_read())
    except Exception as e:
        print("Exception occured", e)
