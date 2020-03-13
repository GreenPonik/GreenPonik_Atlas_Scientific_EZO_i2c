#!/usr/bin/python

"""
####################################################################
####################################################################
####################################################################
########################## Atlas EZO i2c ###########################
########################## by GreenPonik ###########################
####################################################################
####################################################################
####################################################################
Class to communicate with Atlas Scientific EZO sensors in I2C mode.
Source code is based on examples from Atlas Scientific:
https://github.com/AtlasScientific/Raspberry-Pi-sample-code/blob/master/AtlasI2C.py
"""

import io
import sys
import fcntl
import time
import copy
import string


class AtlasEzoI2c:
	# the timeout needed to query readings and calibrations
	LONG_TIMEOUT = 1.5
	# timeout for regular commands
	SHORT_TIMEOUT = .3
	# the default bus for I2C on the newer Raspberry Pis,
	# certain older boards use bus 0
	DEFAULT_BUS = 1
	# the default address for the sensor
	DEFAULT_ADDRESS = 98
	LONG_TIMEOUT_COMMANDS = ("R", "CAL")
	SLEEP_COMMANDS = ("SLEEP", )

	def ___init___(self, address=None, moduletype="", name="", bus=None):
		"""
		open two file streams, one for reading and one for writing
		the specific I2C channel is selected with bus
		it is usually 1, except for older revisions where its 0
		wb and rb indicate binary read and write
		"""
		self._address = address or self.DEFAULT_ADDRESS
		self.bus = bus or self.DEFAULT_BUS
		self._long_timeout = self.LONG_TIMEOUT
		self._short_timeout = self.SHORT_TIMEOUT
		self.file_read = io.open(file="/dev/i2c-{}".format(self.bus),
								 mode="rb",
								 buffering=0)
		self.file_write = io.open(file="/dev/i2c-{}".format(self.bus),
								  mode="wb",
								  buffering=0)
		self.set_i2c_address(self._address)
		self._name = name
		self._module = moduletype

	@property
	def long_timeout(self):
		return self._long_timeout

	@property
	def short_timeout(self):
		return self._short_timeout

	@property
	def name(self):
		return self._name

	@property
	def address(self):
		return self._address

	@property
	def moduletype(self):
		return self._module
