#!/usr/bin/env python3
import init_db
import cv2
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles   # Used for serving static files
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
import numpy as np
import RPi.GPIO as GPIO
import time
# Import the MySQL stuff
import mysql.connector as mysql
from dotenv import load_dotenv
import os
import datetime
# Import for the ADC device
#from ADCDevice import *
# Import for the accelerometer
#from mpu6050 import *
# Import the motor library
from RpiMotorLib import RpiMotorLib
import multiprocessing
import math

''' Environment Variables '''
load_dotenv("credentials.env")

db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

app = FastAPI()

# Mount the static directory
app.mount("/public", StaticFiles(directory="public"), name="public")


# Example route: return the landing HTML page
@app.get("/", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
    with open("Landing_Page.html") as html:
        return HTMLResponse(content=html.read())

# Example route: return the login HTML page
@app.get("login/", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
    with open("Login.html") as html:
        return HTMLResponse(content=html.read())



# Example route: return the register HTML page
@app.get("register/", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
    with open("Register.html") as html:
        return HTMLResponse(content=html.read())



# Example route: return the homepage HTML page
@app.get("home/", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
    with open("Home.html") as html:
        return HTMLResponse(content=html.read())



# Example route: return the specifc product HTML page
@app.get("product/", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
    with open("Product.html") as html:
        return HTMLResponse(content=html.read())

if __name__ == '__main__':
    # Create a Process object and start the process
    #setup()
    #my_process = multiprocessing.Process(target=log_sensors)
    #my_process.start()
    uvicorn.run(app, host='0.0.0.0', port=8000)