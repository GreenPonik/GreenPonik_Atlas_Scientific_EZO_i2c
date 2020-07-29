from setuptools import setup, find_packages
import os
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')


def load_version():
    version_file = os.path.join(os.path.dirname(
        __file__), "GreenPonik_Atlas_Scientific_i2c", "version.py")
    version = {}
    with open(version_file) as fd:
        exec(fd.read(), version)
    return version["__version__"]


setup(
    name="greenponik-atlas-scientific-i2c",
    version=load_version(),
    author="GreenPonik SAS",
    author_email="contact@greenponik.com",
    description="GreenPonik wrapper to use Atlas Scientific on SMBus/I2C",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GreenPonik/GreenPonik_Atlas_Scientific_i2c",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    project_urls={  # Optional
        'Source': 'https://github.com/GreenPonik/GreenPonik_Atlas_Scientific_i2c/',
        'Bug Reports': 'https://github.com/GreenPonik/GreenPonik_Atlas_Scientific_i2c/issues',
    },
    keywords="GreenPonik hydroponics SMBus/i2c EC Electro Conductivity and pH reader Atlas Scientific python hardware diy iot raspberry pi",
    # py_modules=["GreenPonik_Atlas_Scientific_i2c"],
)
