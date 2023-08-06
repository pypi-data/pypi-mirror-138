# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_adxl37x`
================================================================================

A CircuitPython driver for the ADXL37x family of accelerometers


* Author(s): Kattni Rembor

Implementation Notes
--------------------

**Hardware:**

* `ADXL375 - High G Accelerometer (+-200g) <https://www.adafruit.com/product/5374>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit CircuitPython ADXL34x: https://github.com/adafruit/Adafruit_CircuitPython_ADXL34x

"""

from micropython import const
import adafruit_adxl34x

__version__ = "1.0.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ADXL37x.git"

_ADXL375_DEFAULT_ADDRESS = const(0x53)


class DataRate(adafruit_adxl34x.DataRate):  # pylint: disable=too-few-public-methods
    """Stub class for data rate."""


class Range(adafruit_adxl34x.Range):  # pylint: disable=too-few-public-methods
    """Stub class for range."""


class ADXL375(adafruit_adxl34x.ADXL345):
    """
    Driver for the ADXL375 accelerometer

    :param ~busio.I2C i2c: The I2C bus the ADXL375 is connected to.
    :param address: The I2C device address for the sensor. Default is :const:`0x53`.

    **Quickstart: Importing and using the device**

        Here is an example of using the :class:`ADXL375` class.
        First you will need to import the libraries to use the sensor.

        .. code-block:: python

            import board
            import adafruit_adxl37x

        Once this is done you can define your `board.I2C` object and define your sensor object.
        If using the STEMMA QT connector built into your microcontroller,
        use ``board.STEMMA_I2C()``.

        .. code-block:: python

            i2c = board.I2C()  # uses board.SCL and board.SDA
            accelerometer = adafruit_adxl37x.ADXL375(i2c)

        Now you have access to the :attr:`acceleration` attribute.

        .. code-block:: python

            acceleration = accelerometer.acceleration

    """

    def __init__(self, i2c, address=None):
        super().__init__(
            i2c, address if address is not None else _ADXL375_DEFAULT_ADDRESS
        )

    @property
    def range(self):
        """Range is fixed. Updating the range is not implemented."""
        return

    @range.setter
    def range(self, val):
        """Range is fixed. Updating the range is not implemented."""
        raise NotImplementedError("Range not implemented. ADXL375 is fixed at 200G.")
