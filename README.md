[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=alert_status)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)

[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=ncloc)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=duplicated_lines_density)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)

[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=security_rating)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)


![Upload Python Package](https://github.com/GreenPonik/GreenPonik_Atlas_Scientific_i2c/workflows/Upload%20Python%20Package/badge.svg?event=release)


# GreenPonik_Atlas_Scientific_i2c.py Library for Raspberry pi
## A python3 class to use Atlas Scientific EZO circuits on i2c bus.<br>

## ! Only tested on Raspberry Pi 3 A+ !<br>


# Table of Contents

- [GreenPonik_Atlas_Scientific_i2c.py Library for Raspberry pi](#GreenPonikAtlasScientifici2cpy-library-for-raspberry-pi)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Methods](#methods)
- [Examples](#examples)
- [Credits](#credits)


# Installation
```shell
> git clone https://github.com/GreenPonik/GreenPonik_Atlas_Scientific_i2c.git
cd GreenPonik_Atlas_Scientific_i2c
pip3 install -r requirements.txt

or

> pip3 install greenponik-atlas-scientific-i2c
```
```python

from GreenPonik_Altas_Scientific_i2c import AtlasI2c

```

# Examples

## **Read EC**
works with EC circuit https://www.atlas-scientific.com/circuits/conductivity-oem-circuit/<br>

```python
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

```
go to [ec example](examples/read_ec.py)

## **Read pH**
works with pH circuit https://www.atlas-scientific.com/circuits/ph-oem-circuit/<br>

```python
from GreenPonik_Altas_Scientific_i2c import AtlasI2c, CommonsI2c, PHI2c

if __name__ == "__main__":
    try:
        print("get device infos")
        ph_i2c = AtlasI2c(
            address=AtlasI2c.AS_SENSORS_ADDS_TXT_TO_DECIMAL['PH'],
            moduletype="PH",
            name="PH"
        )
        print(CommonsI2c.get_device_info(ph_i2c))
        print(CommonsI2c.get_read(ph_i2c))
    except Exception as e:
        print("Exception occured", e)

```
go to [ph example](examples/read_ph.py)

## todo list
- add calibration workflow in examples
- add compatibility with all circuits (OD / ORP / CO2 / PRESSURE / FLOW)

## Credits
Write by Mickael Lehoux, from [GreenPonik](https://www.greenponik.com), 2020
