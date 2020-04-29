from temperature_client import TemperatureClient
tc = TemperatureClient('greenhouse8266', topic='greenhouse/')
tc.start(10)

