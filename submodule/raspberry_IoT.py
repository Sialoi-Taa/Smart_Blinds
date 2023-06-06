#!/usr/bin/env python3
# IMPORTS -------------------------------------------------------------------------------->
import RPi.GPIO as GPIO
import datetime
import time
import json
import urllib.request


# VARIABLE INITIALIZATION -------------------------------------------------------------------------------->
# Initializing the GPIO pins
GpioPins = [26, 18]


# FUNCTIONS -------------------------------------------------------------------------------->

# The setup function
def setup():
    # Sets the board GPIO
    GPIO.setmode(GPIO.BCM)
    # Set up the relay switch pins
    for pin in GpioPins:
        GPIO.setup(pin,GPIO.OUT)

# Function to turn off circuit and make blinds not clear
def turnOFF():
    for pin in GpioPins:
        GPIO.output(pin,GPIO.LOW)

# Function to turn on circuit and make blinds clear
def turnON():
    for pin in GpioPins:
        GPIO.output(pin,GPIO.HIGH)

# Function to interpret the message fetched from the server and control the circuit connected to the Pi
def interpretation(message:str):
    on = "ON"
    off = "OFF"
    if message is on:
        turnON()
    elif message is off:
        turnOFF()

# IoT Component -------------------------------------------------------------------------------->

try:
    setup()
    url = 'http://localhost:8000/data/'
    serial_name = 'PRODUCT1'
    while(True):
        try:
            response = urllib.request.urlopen(url + serial_name)
            data = response.read().decode('utf-8')
            data = json.loads(data)
            message = data["message"]
            interpretation(message)
        except urllib.error.URLError:
            print("URL not valid!")
        except urllib.error.HTTPError:
            print("HTTP error!")
        time.sleep(5)
except KeyboardInterrupt:
    print('interrupted!')