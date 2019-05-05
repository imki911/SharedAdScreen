# encoding: utf-8
# screenID 113217

import paho.mqtt.client as mqtt
HOST = "test.mosquitto.org" #"101.200.46.138"
PORT = 1883

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("SHIFT_AdScreen113217")


def on_message(client, userdata, msg):
    print(msg.topic+" " + ":" + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(HOST, PORT, 60)
client.loop_forever()
