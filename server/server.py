#!/usr/bin/env python3
# IMPORTS -------------------------------------------------------------------------------->
import init_db
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles   # Used for serving static files
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
import RPi.GPIO as GPIO
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
import bcrypt, secrets 
from pydantic import BaseModel

# VARIABLE INITIALIZATION -------------------------------------------------------------------------------->
''' Environment Variables '''
load_dotenv("credentials.env")
# MySQL variables
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

# Creates the FastAPI object
app = FastAPI()

# Mount the static directory
app.mount("/public", StaticFiles(directory="public"), name="public")

class Registration(BaseModel):
    Email: str
    Username: str
    Password: str

class Login(BaseModel):
    Email: str
    Password: str






# FUNCTIONS -------------------------------------------------------------------------------->
# Function to find the existence of an email
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

# Function to check a user's login info is correct
def check_password(Email, Password):
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("SELECT Password FROM Users WHERE Email=%s", (str(Email)))
    table_password = cursor.fetchone()
    db.close()
    if table_password is not None:
        return bcrypt.checkpw(Password.encode('utf-8'), table_password[0].encode('utf-8'))
    return False

# Function to find the existence of a username
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

# Function to create a new user in the database
def create_user(Username, Password, Email):
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("INSERT INTO Users (Username, Password, Email, created_at) VALUES (%s, %s, %s)", (Username, Password, Email))
    db.commit()
    db.close()

# Function to create a session ID
def create_session(response:Response, Email:str) -> str:
  # Create a session ID
  session_id = secrets.token_urlsafe(16)
  # Connect to mysql
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("SELECT Username FROM Users WHERE Email=%s", (Email))
  username = cursor.fetchone()[0]
  # Delete the previous session for that username
  cursor.execute("DELETE FROM Active_Users WHERE Username='" + username + "';")
  # Insert a new session for that specific user
  query = "INSERT INTO Active_Users (Username, Cookie, created_at) VALUES (%s, %s, %s);" 
  value = (username, session_id, datetime.datetime.now())
  cursor.execute(query, value)
  # Commit to the database
  db.commit()
  # Count how many rows are affected
  count = cursor.rowcount
  # Close the database connection
  db.close()
  # If no rows are affected, return an empty string
  if count == 0:
    return ""
  # Give the client a cookie with the session ID
  response.set_cookie(key="session_id", value=session_id, max_age=900)
  response.set_cookie(key="Username", value=username, max_age=900)
  # Return the session ID as a string
  return session_id

# Function to check the existence of a session ID attached to a username and return what it finds
def check_sessionID(Username: str):
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("SELECT Cookie FROM Active_Users WHERE Username=%s", (Username))
    session_ID = cursor.fetchone()
    db.close()
    if session_ID is None:
        return []
    return session_ID[0]

# Function to use to see if a session should have expired
def expired_session(session_ID):
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("SELECT created_at FROM Active_Users WHERE Cookie=%s", (session_ID))
    start_time = cursor.fetchone()[0]
    db.close()
    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
    end_time = datetime.now()
    time_diff = end_time - start_time
    if(time_diff > 900):
        end_session(session_ID)
        return True
    return False

# Function to end a session and delete it from the database
def end_session(session_id:str) -> bool:
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  query = "DELETE FROM Active_Users WHERE Cookie='" + session_id + "';"
  cursor.execute(query)
  db.commit()
  count = cursor.rowcount
  db.close()
  if count:
    return True
  return False


# ROUTES -------------------------------------------------------------------------------->
# Example route: return the landing HTML page
@app.get("/", response_class=HTMLResponse)
def get_landing_html() -> HTMLResponse:
    with open("views/Landing_Page.html") as html:
        return HTMLResponse(content=html.read())



# Example route: return the login HTML page
@app.get("/login", response_class=HTMLResponse)
def get_login_html(request: Request) -> HTMLResponse:
    session_ID = request.cookies.get('session_id')
    Username = request.cookies.get('Username')
    table_session_ID = check_sessionID(Username)

    if session_ID is not table_session_ID:
        with open("views/Login.html") as html:
            return HTMLResponse(content=html.read())
    else:
        with open("views/Home.html") as html:
            return HTMLResponse(content=html.read())

@app.put("/login")
def verify_login(login: Login, response: Response) -> dict:
    message = {"message": ""}
    Email = login.Email
    Password = login.Password
    success = check_password(Email, Password)
    if success:
        message["message"] = "Success"
        create_session(response, Email)
    else:
        message["message"] = "Failure"
    return message




# Example route: return the register HTML page
@app.get("/register", response_class=HTMLResponse)
def get_register_html() -> HTMLResponse:
    with open("views/Register.html") as html:
        return HTMLResponse(content=html.read())

@app.post("/register")
def register_user(registration: Registration) -> dict:
    # First check to see if the email is in use already
    Email = registration.Email
    Found = find_email(Email)
    # If the email is found, the email is already in use
    if Found:
        message = {"message": "Email already in use"}
        return message
    
    # Second check to see if the username is unique
    Username = registration.Username
    Found = find_username(Username)
    if Found:
        message = {"message": "Username not unique"}
        return message

    # Third encrypt the password
    password = registration.Password
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Lastly create a new user in the database
    create_user(Username, password, Email)
    message = {"message": "Succeess"}
    return message




# Example route: return the homepage HTML page
@app.get("/home", response_class=HTMLResponse)
def get_home_html() -> HTMLResponse:
    with open("views/Home.html") as html:
        return HTMLResponse(content=html.read())



# Example route: return the specifc product HTML page
@app.get("/product", response_class=HTMLResponse)
def get_product_html() -> HTMLResponse:
    with open("views/Product.html") as html:
        return HTMLResponse(content=html.read())

if __name__ == '__main__':
    # Create a Process object and start the process
    #setup()
    #my_process = multiprocessing.Process(target=log_sensors)
    #my_process.start()
    uvicorn.run(app, host='0.0.0.0', port=8000)