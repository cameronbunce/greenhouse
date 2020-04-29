import time
from machine import Pin
from onewire import OneWire
import ds18x20
import binascii

class TemperatureSensor:
    """
    Represents a Temperature sensor
    """
    def __init__(self, pin):
        """
        Finds address of all DS18B20 on bus specified by `pin`
        :param pin: 1-Wire bus pin
        :type pin: int
        """
        self.ds = ds18x20.DS18X20(OneWire(Pin(pin)))
        addr = self.ds.scan()
        if not addr:
            raise Exception('no DS18B20 found at bus on pin %d' % pin)

    def read_temps(self, fahrenheit=True):
        """
        Reads temperature from all DS18X20 sensors available
        :param fahrenheit: Whether or not to return value in Fahrenheit
        :type fahrenheit: bool
        :return: Temperature
        :rtype: dictionary
        """

	addrs = self.ds.scan()
        self.ds.convert_temp()
        time.sleep_ms(750)
	temp = dict()

	for addr in addrs:
		if fahrenheit:
			temp[binascii.hexlify(addr).decode('ascii')] = self.c_to_f(self.ds.read_temp(addr))
		else:
			temp[binascii.hexlify(addr).decode('ascii')] = self.ds.read_temp(addr)

        return temp

    @staticmethod
    def c_to_f(c):
        """
        Converts Celsius to Fahrenheit
        :param c: Temperature in Celsius
        :type c: float
        :return: Temperature in Fahrenheit
        :rtype: float
        """
        return (c * 1.8) + 32


