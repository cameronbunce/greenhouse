# greenhouse
A MQTT sensor network and logging kit to monitor conditions in my greenhouse

The current implementation is a mess of cobbles interfaces but it works. 
It isn't as reliable as I want it though. I am replacing the MQTT implementation with the asynchronous MQTT client by Peter Hinch - https://github.com/peterhinch/micropython-mqtt

Setup - 
Currently the harware setup is an ESP8266 ( though ESP32 is certainly applicable ) 
Any number of DS18B21 sensors can be connected to ESP pin 2 and it will iterate through them and report their reading in degrees F.

The loop.py script includes a map of temperature sensor ID to location description. I'd like to implement this a bit better but it certainly works. Run loop forever and it'll dump your values to InfluxDB on the localhost DB 'greenhouse'

Next on the To-Do list:

-add DHT11/DHT22 sensor support
-add anemometer support
-clean up sensor mapping scheme
-add full implementation guide
