# Python lib to use Atlas Scientific circuit on smbus/i2c

## only tested on Raspberry Pi 3 A+<br>

## works with EC https://www.atlas-scientific.com/circuits/conductivity-oem-circuit/
### Dependencies:
>https://github.com/GreenPonik/GreenPonik_Altas_Scientific_i2c<br>
>https://github.com/GreenPonik/GreenPonik_thermistor_10k
```python
from GreenPonik_Altas_Scientific_i2c import AtlasI2c
from GreenPonik_Atlas_Scientific_i2c.ec_i2c import *
from GreenPonik_thermistor_10k import GreenPonik_thermistor_10k

if __name__ == "__main__":
    print("get device infos")
    ec_i2c = AtlasI2c(address=AtlasI2c.AS_SENSORS_ADDS_TXT_TO_DECIMAL['EC'], moduletype="EC", name="EC")
    print(get_device_info(ec_i2c))
    print("get current temperature compensated")
    print(get_temperature(ec_i2c))
    t = GreenPonik_thermistor_10k.read_temp()
    print(set_temperature(ec_i2c, t))
    print(get_read(ec_i2c))
```
## works with pH https://www.atlas-scientific.com/circuits/ph-oem-circuit/
### Dependencies:
>https://github.com/GreenPonik/GreenPonik_Altas_Scientific_i2c<br>

```python
from GreenPonik_Altas_Scientific_i2c import AtlasI2c
from GreenPonik_Atlas_Scientific_i2c.ph_i2c import *

if __name__ == "__main__":
    print("get device infos")
    ph_i2c = AtlasI2c(address=AtlasI2c.AS_SENSORS_ADDS_TXT_TO_DECIMAL['PH'], moduletype="PH", name="PH")
    print(get_device_info(ph_i2c))
    print(get_read(ph_i2c))
```

### todo list
- add compatibility with all circuits (OD / ORP / CO2 / PRESSURE / FLOW)
- add better readme
- add examples
- add wiring diagram