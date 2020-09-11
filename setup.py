import os
import pathlib
from setuptools import setup, find_packages

# Package meta-data.
NAME = "greenponik-atlas-scientific-oem-i2c"
DESCRIPTION = "GreenPonik library to use Atlas Scientific OEM EC and pH circuits on SMBus/I2C"
URL = "https://github.com/GreenPonik/GreenPonik_Atlas_Scientific_OEM_i2c"
EMAIL = "contact@greenponik.com"
AUTHOR = "GreenPonik SAS"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.0.1"

# What packages are required for this module to be executed?
REQUIRED = [
    # 'requests', 'maya', 'records',
    'adafruit-blinka',
    'adafruit-extended-bus',
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Load the package's version.py module as a dictionary.
about = {}
if not VERSION:
    # project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, "version.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

setup(
    name=NAME,
    version=about["__version__"],
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=("docs")),
    python_requires=REQUIRES_PYTHON,
    project_urls={  # Optional
        'Source': 'https://github.com/GreenPonik/\
        GreenPonik_Atlas_Scientific_i2c/',
        'Bug Reports': 'https://github.com/GreenPonik/\
        GreenPonik_Atlas_Scientific_i2c/issues',
    },
    keywords="GreenPonik hydroponics SMBus/i2c EC Electro Conductivity and pH \
         reader Atlas Scientific OEM python hardware diy iot raspberry pi",
)
