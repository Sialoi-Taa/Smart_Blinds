#!/usr/bin/env python3
# IMPORTS -------------------------------------------------------------------------------->
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
import bcrypt

# VARIABLE INITIALIZATION -------------------------------------------------------------------------------->
''' Environment Variables '''
load_dotenv("credentials.env")

db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

app = FastAPI()

# Mount the static directory
app.mount("/public", StaticFiles(directory="public"), name="public")

# FUNCTIONS -------------------------------------------------------------------------------->
def find_email(Email):
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("SELECT * FROM Users WHERE Email=%s", (str(Email)))
    result = cursor.fetchone()
    db.close()
    if result is None:
        return False
    return True

def find_username(Username):
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("SELECT * FROM Users WHERE Username=%s", (str(Username)))
    result = cursor.fetchone()
    db.close()
    if result is None:
        return False
    return True

def create_user(Username, Password, Email):
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("INSERT INTO Users (Username, Password, Email, created_at) VALUES (%s, %s, %s)", (Username, Password, Email))
    db.commit()
    db.close()

# ROUTES -------------------------------------------------------------------------------->
# Example route: return the landing HTML page
@app.get("/", response_class=HTMLResponse)
def get_landing_html() -> HTMLResponse:
    with open("Landing_Page.html") as html:
        return HTMLResponse(content=html.read())

# Example route: return the login HTML page
@app.get("/login", response_class=HTMLResponse)
def get_login_html() -> HTMLResponse:
    with open("Login.html") as html:
        return HTMLResponse(content=html.read())



# Example route: return the register HTML page
@app.get("/register", response_class=HTMLResponse)
def get_register_html() -> HTMLResponse:
    with open("Register.html") as html:
        return HTMLResponse(content=html.read())

@app.post("/register")
async def register_user(request: Request) -> dict:
    registration = await request.json()
    # First check to see if the email is in use already
    Email = registration["Email"]
    Found = find_email(Email)
    # If the email is found, the email is already in use
    if Found:
        message = {"message": "Email already in use"}
        return message
    
    # Second check to see if the username is unique
    Username = registration["Username"]
    Found = find_username(Username)
    if Found:
        message = {"message": "Username not unique"}
        return message

    # Third encrypt the password
    password = registration["Password"]
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Lastly create a new user in the database
    create_user(Username, password, Email)
    message = {"message": "Succeess"}
    return message


# Example route: return the homepage HTML page
@app.get("/home", response_class=HTMLResponse)
def get_home_html() -> HTMLResponse:
    with open("Home.html") as html:
        return HTMLResponse(content=html.read())



# Example route: return the specifc product HTML page
@app.get("/product", response_class=HTMLResponse)
def get_product_html() -> HTMLResponse:
    with open("Product.html") as html:
        return HTMLResponse(content=html.read())

if __name__ == '__main__':
    # Create a Process object and start the process
    #setup()
    #my_process = multiprocessing.Process(target=log_sensors)
    #my_process.start()
    uvicorn.run(app, host='0.0.0.0', port=8000)