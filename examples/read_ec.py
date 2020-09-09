from GreenPonik_Atlas_Scientific_i2c.GreenPonik_Altas_Scientific_i2c import AtlasI2c, ECI2c

if __name__ == "__main__":
    try:
        print("get device infos")
        i2c_device = AtlasI2c(
            address=AtlasI2c.ADDR_EZO_TXT_TO_HEXA['EC'],
            moduletype="EC",
            name="EC"
        )
        ec_i2c = ECI2c(i2c_device)
        print(ec_i2c.get_device_info())
        print("get current temperature compensated")
        print(ec_i2c.get_temperature())
        # put here the current temperature
        print(ec_i2c.set_temperature(25.00))
        ec = ec_i2c.get_read()
        print("current ec is %.2f" % ec)
    except Exception as e:
        print("Exception occured", e)
