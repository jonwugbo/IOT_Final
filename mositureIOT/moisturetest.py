# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import paho.mqtt.client as mqtt
from adafruit_seesaw.seesaw import Seesaw

#Define MQTT Variables
MQTT_HOST = "10.0.0.90"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 5
MQTT_TOPIC = "iot"

# Define on_connect event handler
def on_connect(mosq, obj, rc):
       print ("Connected to MQTT Broker")

def on_publish(client, userdata, mid):
       print ("Message published...")

#Initiate MQTT Client
mqttc = mqtt.Client()

#Register Event handlers
mqttc.on_publish = on_publish
mqttc.on_connect = on_connect

i2c_bus = board.I2C()  # uses board.SCL and board.SDA
# i2c_bus = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

ss = Seesaw(i2c_bus, addr=0x36)

while True:
    mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    # read moisture level through capacitive touch pad
    touch = ss.moisture_read()

    # read temperature from the temperature sensor
    temp = ss.get_temp()
    data = "temperature,sensor=moisture temp_c=" + str(temp) + ",moisture=" + str(touch)
    mqttc.publish(MQTT_TOPIC,data)

    #print(data)
    time.sleep(5)

    mqttc.disconnect()
