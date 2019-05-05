# encoding: utf-8

import paho.mqtt.client as mqtt
import sys
import json

HOST = "broker.hivemq.com"#(see http://www.mqtt-dashboard.com/)  #"test.mosquitto.org" #"101.200.46.138"
PORT = 1883

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid):
    print('pub success')
    client.disconnect()
    #print(msg.topic+" "+str(msg.payload))


def pub(screenId,imageUrl):
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(HOST, PORT, 60)
    client.publish("SHIFT_AdScreen"+str(screenId),payload = imageUrl,qos=2) # 发布一个主题为'chat'
    #client.loop_start()
    client.loop_forever()
 
if __name__ == '__main__':

    #usage: publish.py <screen ID> <image Url> 
    if len(sys.argv) != 3:
        print('''usage: publish.py <screen ID> <image Url>''')
        exit()
    screenId=sys.argv[1]
    #print("SHIFT_AdScreen"+str(screenId))
    imageUrl=sys.argv[2]
 
    pub(screenId,imageUrl)
    print('Send success')
