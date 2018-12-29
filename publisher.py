import json
import paho.mqtt.client as mqtt

broker = "tts.toannhu.com"
port = 8080
topic = "myTopic"
# topic = "smartFarm"

#create function for callback
def on_publish(client,userdata,result):
    print("Data published \n")
    pass

# create client object
client = mqtt.Client(transport='websockets')
# assign function to callback
client.on_publish = on_publish
# establish connection
client.connect(broker,port)	
# publish
mes = { "id": 1, "name": "node_3", "day": 2, "temp": 50, "humd": 80, "light": 20 }
res = client.publish(topic,json.dumps(mes))	

# import paho.mqtt.client as mqtt #import the client1
# import time
# ############
# def on_message(client, userdata, message):
#     print("message received " ,str(message.payload.decode("utf-8")))
#     print("message topic=",message.topic)
#     print("message qos=",message.qos)
#     print("message retain flag=",message.retain)
# ########################################
# broker_address="192.168.1.184"
# #broker_address="iot.eclipse.org"
# print("creating new instance")
# client = mqtt.Client("P1") #create new instance
# client.on_message=on_message #attach function to callback
# print("connecting to broker")
# client.connect(broker_address) #connect to broker
# client.loop_start() #start the loop
# print("Subscribing to topic","house/bulbs/bulb1")
# client.subscribe("house/bulbs/bulb1")
# print("Publishing message to topic","house/bulbs/bulb1")
# client.publish("house/bulbs/bulb1","OFF")
# time.sleep(4) # wait
# client.loop_stop() #stop the loop