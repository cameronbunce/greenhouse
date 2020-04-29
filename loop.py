import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

SensorMap = {"28aa727f4a140183":"Water", "28aa9a7e4a1401e8":"Ground", "28aa91814a140173":"Air", "28aa21a14a14014c":"Jade"}
def on_connect(client, userdata, flags, rc):
   print("Connected with result code "+str(rc))
   client.subscribe("greenhouse/#")

def on_message(client, userdata, msg):
   print(msg.topic+" "+str(msg.payload.decode('ascii')))
   json_body = [
   {
      "measurement": "temperature",
      "tags": {
         "sensor": SensorMap[msg.topic[11:27]],
      },
      "fields": {
         "value": str(msg.payload.decode('ascii'))
      }
   }
   ]

   influx_client.write_points(json_body)
#   print(msg.topic+" "+str(msg.payload))

def republish(client, userdata, msg):
# take in bulk and republish to individual sensor topics
   temperatures = dict(msg.payload.decode("ascii").split(","))
   for sensor, temperature in temperatures:
      publish("greenhouse/"+str(sensor)+"/temperature", tempertature)



influx_client = InfluxDBClient('localhost', 8086, database='greenhouse')
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.message_callback_add("greenhouse/sensor/temperature", republish)
client.connect("localhost", 1883, 60)

client.loop_forever()
