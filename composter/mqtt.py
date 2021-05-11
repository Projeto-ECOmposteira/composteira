import paho.mqtt.client as mqtt
import json
from .models import *

def on_connect(client, userdata, flags, rc):
    client.subscribe("ecomposteira/composter/measurements")

def on_message(client, userdata, msg):
    try:
        temp = msg.payload.decode('utf8').replace("'", '"')
        data = json.loads(temp)
        composter = Composter.objects.get(macAddress=data['macAddress'])
        data.pop('macAddress')
        measurement = Measurement.objects.create(composter=composter, **data)
        measurement.trigger_alerts()
    except Exception:
        pass

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)