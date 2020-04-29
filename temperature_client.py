import time
#import json

from umqtt.robust import MQTTClient

from temperature import TemperatureSensor

from machine import WDT

class TemperatureClient:
    """
    Represents an MQTT client which publishes temperature data on an interval
    """

    def __init__(self, client_id, server='192.168.1.215', pin=2, fahrenheit=True, topic=None,
                 **kwargs):
        """
        Instantiates a TemperatureSensor and MQTTClient; connects to the
        MQTT broker.
        Arguments `server` and `client_id` are required.

        :param client_id: Unique MQTT client ID
        :type client_id: str
        :param server: MQTT broker domain name / IP
        :type server: str
        :param pin: 1-Wire bus pin
        :type pin: int
        :param fahrenheit: Whether or not to publish temperature in Fahrenheit
        :type fahrenheit: bool
        :param topic: Topic to publish temperature on
        :type topic: str
        :param kwargs: Arguments for MQTTClient constructor
        """
        self.sensor = TemperatureSensor(pin)
        self.client = MQTTClient(client_id, server, **kwargs)
        if not topic:
            self.topic = 'devices/%s/temperature/degrees' % \
                         self.client.client_id
        else:
            self.topic = topic
        self.fahrenheit = bool(fahrenheit)

        self.client.connect()

    def publishTemperature(self):
        """
        Reads the current temperature and publishes a JSON payload on the
	configured topic, e.g., '{"unit": "F", "degrees": "72.5"}'
        """
        payload = self.sensor.read_temps(self.fahrenheit)
        """
	if self.fahrenheit:
		payload['unit'] = 'F'
	else:
		payload['unit'] = 'C'
        """
        for sen in payload:
            self.client.publish(self.topic+str(sen)+"/temperature", str(payload[sen]))
            print(str(sen)+" "+str(payload[sen]))

    def start(self, interval=60):
        """
        Begins to publish temperature data on an interval (in seconds).
        This function will not exit! Consider using deep sleep instead.
        :param interval: How often to publish temperature data (60s default)
        :type interval: int
        """
        wdt = WDT()
        while True:
            self.publishTemperature()
            time.sleep(interval)
            wdt.feed()



