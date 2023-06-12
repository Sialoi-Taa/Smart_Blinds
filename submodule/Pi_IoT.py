#!/usr/bin/env python3

import RPi.GPIO as GPIO
import subprocess
import sys
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import threading
import time
import urllib.request
import json

# Network prompt url = http://192.168.4.1:8000

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class Network(BaseModel):
    ssid: str
    password: str

GpioPins = [24, 19]

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

# A Function to connect to WiFi with the form data given
def Prompt_Connection(ssid, password):
    """
    List of sources that was referenced to complete this function:
    https://raspberrypi.stackexchange.com/questions/135809/raspi-connect-to-wifi-via-python-os-shell-commands
    https://www.radishlogic.com/linux/how-to-connect-to-wifi-using-nmcli/
    https://www.geeksforgeeks.org/executing-shell-commands-with-python/
    https://forums.raspberrypi.com/viewtopic.php?t=216506
    https://askubuntu.com/questions/733469/what-is-the-difference-between-systemctl-start-and-systemctl-enable

    Here's how the function works. First it is assumed that the Pi is in network hosting mode.
    So we switch out of network hosting and go into network searching and connecting mode.
    Using the subprocess.run() commands, we can write to the terminal commands and when the
    first two subprocess.run() commands finish, the Pi will stop hosting a network.
    The last subprocess.run() command will connect the Pi to the SSID provided by the user.
    After that, the Pi will use the internet to throw GET fetches to obtain routine commands
    from the server.
    """
    # Sleep for 1 second to let the program return something back to the user first
    time.sleep(1)
    # Stop the access point
    # This undos the process at start up that would make the Pi become an access point
    subprocess.run(["sudo", "systemctl", "stop", "hostapd"])
    subprocess.run(["sudo", "systemctl", "stop", "dnsmasq"])

    # Connect to the Wi-Fi network
    # Using NetworkManager
    subprocess.run(["sudo", "nmcli", "device", "wifi", "connect", ssid, "password", password], capture_output=True)
    try:
        time.sleep(2)
        # Serial
        serial = 'PROTOTYPE'
        # Ngrok URL
        the_url = 'https://9e1c-69-196-43-207.ngrok-free.app'
        while(True):
            # URL fetches
            response = urllib.request.urlopen(f"{the_url}/data/{serial}")
            response = response.read().decode('utf-8')
            response = json.loads(response)
            interpretation(response["message"])
            print(response)
            time.sleep(3)
    except KeyboardInterrupt:
        pass
    pass

# A route to the landing page
@app.get("/", response_class=HTMLResponse)
def get_network() -> HTMLResponse:
    with open("network_prompt.html") as html:
        return HTMLResponse(content=html.read())

# A route that handles form submission
@app.post("/network_information")
async def login(info: Network):
    # Assigns ssid variables correctly
    ssid = info.ssid
    password = info.password

    # If the password is nothing, change it to an empty string
    if password is None:
        password = ""
    file_path = 'network.txt'

    # Removes existing saved network data
    if os.path.exists(file_path):
        os.remove(file_path)

    # Writes a new network saved file
    with open(file_path, 'w') as file:
        file.write(f'{ssid}\n')
        file.write(f'{password}')

    # Connects to the new network
    # Create a thread object
    my_thread = threading.Thread(target=Prompt_Connection, args=(ssid, password))
    my_thread.start()

    # Returns the status of the network saved back to the user while the thread is being ran
    return "Network saved, thank you!"


if __name__ == '__main__':
     uvicorn.run(app, host='0.0.0.0', port=8000)
