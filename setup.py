import os
from setuptools import setup, find_packages


def here(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def load_version():
    version_file = os.path.join(os.path.dirname(
        __file__), "src/atlas_ezo_i2c", "version.py")
    version = {}
    with open(version_file) as fd:
        exec(fd.read(), version)
    return version["__version__"]


def long_description():
    with open("readme.md", "r") as fd:
        return fd.read()


setup(
    name="atlas-ezo-i2c",
    description="Atlas Scientific EZO I2C",
    url="https://github.com/GreenPonik/GreenPonik_atlas_scientific_i2c",
    author="GreenPonik SAS",
    author_email="contact@greenponik.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    version=load_version(),
    long_description=long_description(),
    long_description_content_type="text/markdown",
)
