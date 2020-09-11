from GreenPonik_Altas_Scientific_OEM_i2c.GreenPonik_ECI2c import ECI2c

if __name__ == "__main__":
    try:
        print("get device infos")
        ec_i2c = ECI2c(
            bus=1,
            addr=ECI2c.ADDR_OEM_TXT_TO_HEXA['EC'],
            moduletype="EC",
        )
        print(ec_i2c.get_device_info())
        # put here the current temperature
        print(ec_i2c.set_temperature(25.00))
        ec = ec_i2c.get_read()
        print("current ec is %.2f" % ec)
    except Exception as e:
        print("Exception occured", e)
