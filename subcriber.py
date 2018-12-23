import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("myTopic")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
	a = True

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

from threading import Thread
from time import sleep

a = False

def threaded_function():
	global a
	while True:
		if (a):
			print("hello phuc")
		sleep(1)

def mqtt_function(): 
	global a
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("localhost", 1883, 60)
	while True:
		client.loop_start()
		

thread = Thread(target = mqtt_function)
thread2 = Thread(target = threaded_function)
thread.start()
thread2.start()