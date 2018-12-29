#!/usr/bin/python

import sys
import json
import datetime
import paho.mqtt.client as mqtt

manual = 0

def pass_to_func_and_pub(data_to_pub):
    try:
        mes = json.loads(data_to_pub)
    except Exception as e:
        print("Couldn't parse raw data: %s" % data_to_pub, e)
    else:
        return mes

def on_connect(mqttc, obj, flags, rc):
    print("Connection returned result: " + str(rc))

def on_message(mqttc, obj, msg):
	global manual
	mes = pass_to_func_and_pub(msg.payload.decode('utf-8'))
	if (mes["type"] == "sensor" and manual == 0):
		temperature = mes["temp"]
		w_temp_max = mes["w_temp_max"]
		w_temp_min = mes["w_temp_min"]
		humidity = mes["humd"]
		w_humd = mes["w_humd"]
		light = mes["light"]
		w_light = mes["w_light"]
		test_time = datetime.datetime.now().time().strftime('%H')
		if (test_time >= "7" and test_time <= "16"):
			time_s = 1
		else:
			time_s = 0
		if (manual == 0):
			if (temperature>=w_temp_max):
				# GPIO.output(24, 1)
				print("Temp >= temp_max Led 1 on")
			elif (temperature<w_temp_max):
				# GPIO.output(24, 0)
				print("Temp <= temp_max Led 1 on")
			if (humidity < w_humd):
				# GPIO.output(23, 0)
				print("Humd < w_humd Pump on")
			elif (humidity > w_humd):
				# GPIO.output(23, 1)
				print("Humd < w_humd Pump off")
			if (light < w_light and time_s == 1):
				# GPIO.output(25, 1)
				print("Light < w_light Led 2 on")
			else: 
				# GPIO.output(25, 0)
				print("Light < w_light Led 2 off")
	elif (mes["type"] == "control"):
		if (manual == 1):
			if (mes["device"] == "w_pump" and mes["status"] == 1):
				# GPIO.output(23, 0)
				print("Pump on")
			elif (mes["device"] == "w_pump" and mes["status"] == 0):
				# GPIO.output(23, 1)
				print("Pump off")
			if (mes["device"] == "w_led_1" and mes["status"] == 1):
				# GPIO.output(24, 1)
				print("Led 1 on")
			elif (mes["device"] == "w_led_1" and mes["status"] == 0):
				# GPIO.output(24, 0)
				print("Led 1 off")
			if (mes["device"] == "w_led_2" and mes["status"] == 1):
				# GPIO.output(25, 1)
				print("Led 2 on")
			elif (mes["device"] == "w_led_2" and mes["status"] == 0):
				# GPIO.output(25, 0)
				print("Led 2 off")
		elif (manual == 0 and mes["device"] == "manual" and mes["status"] == 1):
			manual = 1
			print("Change manual to control status 1")
	# print(mes["node"])
	# print(mes["device"])
	# print(mes["status"])
	# print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

mqttc = mqtt.Client(transport='websockets')   
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.connect("tts.toannhu.com", 8080, 60)

mqttc.subscribe("smartFarm", 0)

mqttc.loop_forever()
