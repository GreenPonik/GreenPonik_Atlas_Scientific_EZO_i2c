from GreenPonik_Atlas_Scientific_i2c import AtlasI2c, CommonsI2c, ECI2c

if __name__ == "__main__":
    try:
        print("get device infos")
        ec_i2c = AtlasI2c(
            address=AtlasI2c.AS_SENSORS_ADDS_TXT_TO_DECIMAL['EC'],
            moduletype="EC",
            name="EC"
        )
        print(CommonsI2c.get_device_info(ec_i2c))
        print("get current temperature compensated")
        print(CommonsI2c.get_temperature(ec_i2c))
        # put here the current temperature
        print(CommonsI2c.set_temperature(ec_i2c, 25.00))
        ec = CommonsI2c.get_read(ec_i2c)
        print("current ec is %.2f" % ec)
    except Exception as e:
        print("Exception occured", e)
