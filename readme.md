[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=alert_status)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)

[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=ncloc)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=duplicated_lines_density)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)

[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=security_rating)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)


![Upload Python Package](https://github.com/GreenPonik/GreenPonik_OneWire_DS18B20/workflows/Upload%20Python%20Package/badge.svg?event=release)


# GreenPonik_Atlas_Scientific_i2c.py Library for Raspberry pi
---------------------------------------------------------
this is a python lib to use Atlas Scientific circuits on smbus/i2c bus.

## Table of Contents

- [GreenPonik_Atlas_Scientific_i2c.py Library for Raspberry pi](#h2-id%2222greenponikatlasscientifici2cpy-library-for-raspberry-pi-4%22greenponikatlasscientifici2cpy-library-for-raspberry-pih2)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Examples](#examples)
- [Credits](#credits)


## Installation
>git clone https://github.com/GreenPonik/GreenPonik_Atlas_Scientific_i2c.git
```python
from GreenPonik_Altas_Scientific_i2c import AtlasI2c
```

## ! Only tested on Raspberry Pi 3 A+ !<br>

## Examples

### Read EC
works with EC https://www.atlas-scientific.com/circuits/conductivity-oem-circuit/<br>
#### Dependencies:
>https://github.com/GreenPonik/GreenPonik_Altas_Scientific_i2c<br>
>https://github.com/GreenPonik/GreenPonik_thermistor_10k<br>

```python
from GreenPonik_Altas_Scientific_i2c import AtlasI2c, ec_i2c
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

### Read pH
works with pH https://www.atlas-scientific.com/circuits/ph-oem-circuit/<br>
#### Dependencies:
>https://github.com/GreenPonik/GreenPonik_Altas_Scientific_i2c<br>

```python
from GreenPonik_Altas_Scientific_i2c.GreenPonik_Altas_Scientific_i2c import AtlasI2c
from GreenPonik_Atlas_Scientific_i2c.ph_i2c import *

if __name__ == "__main__":
    print("get device infos")
    ph_i2c = AtlasI2c(address=AtlasI2c.AS_SENSORS_ADDS_TXT_TO_DECIMAL['PH'], moduletype="PH", name="PH")
    print(get_device_info(ph_i2c))
    print(get_read(ph_i2c))
```


## todo list
- add calibration workflow in examples
- package it on pypi
- add compatibility with all circuits (OD / ORP / CO2 / PRESSURE / FLOW)

## Credits
Write by Mickael Lehoux, from [GreenPonik](https://www.greenponik.com), 2020