[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=alert_status)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)

[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=ncloc)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=duplicated_lines_density)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)

[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=security_rating)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_Atlas_Scientific_i2c&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_Atlas_Scientific_i2c)


![Upload Python Package](https://github.com/GreenPonik/GreenPonik_Atlas_Scientific_i2c/workflows/Upload%20Python%20Package/badge.svg?event=release)


# GreenPonik_Atlas_Scientific_i2c.py Library for Raspberry pi
## A python3 class to use Atlas Scientific OEM circuits on i2c bus.<br>

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
> git clone https://github.com/GreenPonik/GreenPonik_Atlas_Scientific_OEM_i2c.git
cd GreenPonik_Atlas_Scientific_OEM_i2c
pip3 install -r requirements.txt

or

> pip3 install greenponik-atlas-scientific-oem-i2c
```
```python

from GreenPonik_Altas_Scientific_i2c.GreenPonik_Altas_Scientific_OEM_i2c import (
    ECI2c,
    PHI2c,
)
```

# Examples

## **Read EC**
works with EC circuit https://www.atlas-scientific.com/circuits/conductivity-oem-circuit/<br>

```python
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

```
go to [ec example](examples/read_ec.py)

## **Read pH**
works with pH circuit https://www.atlas-scientific.com/circuits/ph-oem-circuit/<br>

```python
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

```
go to [ph example](examples/read_ph.py)

## todo list
- add calibration workflow in examples
- add compatibility with all circuits (OD / ORP / CO2 / PRESSURE / FLOW)

## Credits
Write by Mickael Lehoux, from [GreenPonik](https://www.greenponik.com), 2020
