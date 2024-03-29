#!/usr/bin/env python3
# IMPORTS -------------------------------------------------------------------------------->
import init_db
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles   
import mysql.connector as mysql
from dotenv import load_dotenv
import os
import datetime
import bcrypt, secrets 
from pydantic import BaseModel
from urllib.request import urlopen


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
app.mount("/views", StaticFiles(directory="views"), name="views")

# Pydantic models for form data
class Registration(BaseModel):
    Email: str
    Username: str
    Password: str

class Login(BaseModel):
    Email: str
    Password: str

class Owner(BaseModel):
    Serial_Number: str
    Product_Name: str

class Schedule(BaseModel):
    Start_Time: str
    End_Time: str
    State: str


# FUNCTIONS -------------------------------------------------------------------------------->

# Function to find the existence of an email
def find_email(Email:str):
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    #db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("SELECT * FROM Users WHERE Email=%s", (str(Email),))
    result = cursor.fetchone()
    db.close()
    if result is None:
        return False
    return True

# Function to check a user's login info is correct
def check_password(Email:str, Password:str) -> bool:
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("SELECT Password FROM Users WHERE Email=%s", (str(Email),))
    table_password = cursor.fetchone()
    db.close()
    if table_password is not None:
        return bcrypt.checkpw(Password.encode('utf-8'), table_password[0].encode('utf-8'))
    return False

# Function to find the existence of a username
def find_username(Username:str) -> bool:
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("SELECT * FROM Users WHERE Username=%s", (str(Username),))
    result = cursor.fetchone()
    db.close()
    if result is None:
        return False
    return True

# Function to find the serial in the Owners table through product name and username 
def return_serial(Username:str, Product_Name:str) -> str:
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("SELECT Serial FROM Owners WHERE Username=%s AND Product_Name=%s", (str(Username), str(Product_Name),))
    result = cursor.fetchone()[0]
    db.close()
    return result

# Function to create a new user in the database
def create_user(Username:str, Password:str, Email:str):
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("INSERT INTO Users (Username, Password, Email) VALUES (%s, %s, %s)", (Username, Password, Email,))
    db.commit()
    db.close()

# Function to create a session ID
def create_session(response:Response, Email:str) -> str:
    # Create a session ID
    session_id = secrets.token_urlsafe(16)
    # Connect to mysql
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("SELECT Username FROM Users WHERE Email=%s", (str(Email),))
    username = cursor.fetchone()[0]
    # Delete the previous session for that username
    cursor.execute("DELETE FROM Active_Users WHERE Username=%s;", (str(username),))
    # Insert a new session for that specific user
    cursor.execute("INSERT INTO Active_Users (Username, Cookie, created_at) VALUES (%s, %s, %s);", (str(username), str(session_id), str(datetime.datetime.now()),))
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
def check_sessionID(Username:str, session_id:str) -> bool:
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("SELECT Cookie FROM Active_Users WHERE Username=%s", (Username,))
    session_ID = cursor.fetchone()
    db.close()
    if ((session_ID is None) or (session_ID is not session_id)):
        return False
    return True

# Function to use to see if a session should have expired
def expired_session(session_ID:str) -> bool:
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("SELECT created_at FROM Active_Users WHERE Cookie=%s", (session_ID,))
    start_time = cursor.fetchone()[0]
    db.close()

    end_time = datetime.datetime.now()
    time_diff = end_time - start_time
    if(time_diff.total_seconds() > 830.0):
        end_session(session_ID)
        return True
    return False

# Function to end a session and delete it from the database
def end_session(session_id:str) -> bool:
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("DELETE FROM Active_Users WHERE Cookie=%s;", (session_id,))
    db.commit()
    count = cursor.rowcount
    db.close()
    if count:
        return True
    return False

# Function to delete a serial from the unregistered table
def delete_unregistered_serial(serial_number:str) -> bool:
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("SELECT EXISTS(SELECT * FROM Unregistered WHERE Serial=%s);", (serial_number,))
    result = cursor.fetchall()
    if result[0][0] == 1:
        cursor.execute("DELETE FROM Unregistered WHERE Serial=%s;", (serial_number,))
        db.commit()
        db.close()
        return True
    else:
        db.close()
        return False

# Function to add an owner
def add_owner(username:str, product_name:str, serial_number:str) -> bool:
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("INSERT INTO Owners (Username, Serial, Product_Name) VALUES (%s, %s, %s);", (username, serial_number, product_name,))
    db.commit()
    count = cursor.rowcount
    db.close()
    if count == 0:
        return False
    return True

# Function to unregister a product
def unregister_product(serial_number) -> bool:
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")

    # Delete the attachment between product and user
    cursor.execute("DELETE FROM Owners WHERE Serial=%s;", (serial_number,))
    db.commit()
    count = cursor.rowcount
    if count == 0:
        db.close()
        return False
    cursor.execute("INSERT INTO Unregistered (Serial) VALUES (%s);", (serial_number,))
    db.commit()
    count = cursor.rowcount
    db.close()
    if count == 0:
        return False
    return True

# A function for getting all of the products under a user's account
def get_user_products(Username:str) -> list:
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("SELECT Serial, Product_Name FROM Owners WHERE Username=%s", (Username,))
    # Will be in the form results[rows][columns]
    results = cursor.fetchall()
    db.close()

    # If there's no products under the user's name, then return nothing
    if len(results) == 0:
        return []
    return results

# A function for checking the state of a product in the MySQL tables
def check_state_product(Username:str, product_name:str) -> bool:
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("SELECT Serial FROM Owners WHERE Username=%s AND Product_Name=%s", (Username, product_name,))
    serial = cursor.fetchone()[0]
    cursor.execute("SELECT State FROM State WHERE Serial=%s", (serial,))
    state = cursor.fetchone()[0]
    db.close()
    if state:
        return True
    return False

# A function updating the state of a product in the MySQL tables
def update_state(Username:str, product_name:str, state:int) -> bool:
    if state == 1:
        state = 0
    else:
        state = 1
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("SELECT Serial FROM Owners WHERE Username=%s AND Product_Name=%s", (Username, product_name,))
    serial = cursor.fetchone()[0]
    cursor.execute("UPDATE State SET State=%s WHERE Serial=%s", (str(state), serial,))
    db.commit()
    db.close()
    if state:
        return True
    else:
        return False

# A function for adding a new schedule
def add_schedule(start_time:str, end_time:str, state:str, serial:str) -> bool:
    if state == "ON":
        state = 1
    else:
        state = 0
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("INSERT INTO Schedule (Serial, Start_Time, End_Time, State) VALUES (%s, %s, %s, %s)", (serial, start_time, end_time, state,))
    db.commit()
    count = cursor.rowcount
    db.close()
    if count:
        return True
    return False

# A function for getting all of the products under a user's account
def load_schedules(Serial:str) -> list:
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("SELECT Start_Time, End_Time, State FROM Schedule WHERE Serial=%s", (Serial,))
    # Will be in the form results[rows][columns]
    results = cursor.fetchall()
    db.close()

    # If there's no products under the user's name, then return nothing
    if len(results) == 0:
        return []
    return results

# A function for checking to see if the product needs to be turned on or off
def schedule_check(serial: str) -> str:
    message = ""
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("SELECT Start_Time, End_Time, State FROM Schedule WHERE Serial=%s", (serial,))
    results = cursor.fetchall()

    # Iterate through all of the schedules found
    current_time = datetime.datetime.now()
    for row in results:
        start_time_hour = int(row[0][:2])
        start_time_min  = int(row[0][3:])
        state = row[2]
        # Logic for scheduling
        # When the current time matches the time for the start time of a schedule, the state will change
        # By making it this way, we can give the toggle feature priority 
        if(start_time_hour == current_time.hour and start_time_min == current_time.minute):
            if state:
                message = "ON"
            else:
                message = "OFF"
            # Update the state table
            cursor.execute("UPDATE State SET State=%s WHERE Serial=%s", (str(state), serial,))
            db.commit()
            break    
    db.close()
    return message

# A function for checking the state of a product in the MySQL tables
def state_check(Serial: str) -> bool:
    db = mysql.connect(user=db_user, database=db_name, password=db_pass, host=db_host, auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("USE Smart_Blinds;")
    cursor.execute("SELECT State FROM State WHERE Serial=%s", (Serial,))
    state = cursor.fetchone()[0]
    db.close()
    if state:
        return True
    return False




# ROUTES -------------------------------------------------------------------------------->
# A route to the landing page
@app.get("/", response_class=HTMLResponse)
def get_landing_html() -> HTMLResponse:
    with open("views/Landing_Page.html") as html:
        return HTMLResponse(content=html.read())



# A route for leading the user to a home page if they have a session ID already or the login HTML page
@app.get("/login", response_class=HTMLResponse)
def get_login_html(request: Request, response: Response) -> HTMLResponse:
    session_ID = request.cookies.get('session_id')
    Username = request.cookies.get('Username')
    if session_ID is None or Username is None:
        with open("views/Login.html") as html:
            return HTMLResponse(content=html.read())

    success = check_sessionID(Username, session_ID)

    if not success:
        with open("views/Login.html") as html:
            return HTMLResponse(content=html.read())
    else:
        with open("views/Home.html") as html:
            return HTMLResponse(content=html.read())

# A route for processing the user's login information
@app.put("/login")
def verify_login(login: Login, response: Response) -> dict:
    message = {}
    Email = login.Email
    Password = login.Password
    success = check_password(Email, Password)
    if success:
        message["message"] = "Success"
        create_session(response, Email)
    else:
        message["message"] = "Failure"
    return message




# A route for giving the user the registration HTML page
@app.get("/register", response_class=HTMLResponse)
def get_register_html() -> HTMLResponse:
    with open("views/Register.html") as html:
        return HTMLResponse(content=html.read())

# A route that processes the user's registration data
@app.post("/register") # registration: Registration request: Request
async def register_user(registration: Registration) -> dict:
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




# A route for getting the HTML page for the user's home page and their list of products
@app.get("/home", response_class=HTMLResponse)
def get_home_html() -> HTMLResponse:
    with open("views/Home.html") as html:
        return HTMLResponse(content=html.read())

# A route for attaching a product to a user's account
@app.post("/home")
def add_product(owner: Owner, request: Request) -> dict:
    message = {}
    Serial_Number = owner.Serial_Number
    Product_Name = owner.Product_Name
    Username = request.cookies.get("Username")
    #print(Username)

    # Attempting to delete the serial number
    success = delete_unregistered_serial(Serial_Number)
    if not success:
        message["message"] = "Serial number doesn't exist or is already owned"
        return message
    
    # Serial number was deleted successfully and ready to be added to a user's account
    success = add_owner(Username, Product_Name, Serial_Number)
    if not success:
        message["message"] = "Serial number was not added to the owner"
        return message
    message["message"] = "Success"
    return message

# A route to unattach a product from a user's account
@app.delete("/home")
def delete_ownership(data: dict) -> dict:
    message = {}
    Serial_number = data["Serial_Number"]
    success = unregister_product(Serial_number)
    if not success:
        message["message"] = "Failure"
    else:
        message["message"] = "Success"
    return message

# A route for getting all of the products under a specfic username
@app.get("/home/products")
def get_products(request: Request) -> list:
    username = request.cookies.get("Username")
    #print(username)
    products = get_user_products(username)
    return products
        
# A route to check if a session is active, expired, or doesn't exist
@app.get("/sessions")
def check_session(request: Request, response: Response) -> dict:
    session_id = request.cookies.get("session_id")
    username = request.cookies.get("Username")
    message = {}
    if((session_id is None or username is None)):
        message["message"] = "Session doesn't exist"
        return message
    success = expired_session(session_id)
    if(success):
        message["message"] = "Session Expired"
        end_session(session_id)
        response.delete_cookie(key="session_id")
        response.delete_cookie(key="Username")
    else:
        message["message"] = "Session Active"
    return message
    







# A route to the product specific page
@app.get("/product", response_class=HTMLResponse)
def get_product_html() -> HTMLResponse:
    with open("views/Product.html") as html:
        return HTMLResponse(content=html.read())

# A route to get all of the schedules assigned to one product
@app.get("/schedule")
def schedule_loader(request: Request) -> list:
    Username = request.cookies.get("Username")
    Product_Name = request.cookies.get("Product_Name")
    serial = return_serial(Username, Product_Name)
    schedules = load_schedules(serial)
    # [row][start_time, end_time, state]
    return schedules
    

# A route for getting the current state of the blinds
@app.get("/state")
def check_state(request: Request) -> dict:
    message = {}
    Username = request.cookies.get("Username")
    Product_Name = request.cookies.get("Product_Name")
    success = check_state_product(Username, Product_Name)
    if success:
        message["message"] = "ON"
    else:
        message["message"] = "OFF"
    return message

# A route for updating the state of the Smart Blinds
@app.put("/state")
def update_the_state(request: Request) -> dict:
    message = {}
    Username = request.cookies.get("Username")
    Product_Name = request.cookies.get("Product_Name")
    success = check_state_product(Username, Product_Name)

    if success:
        state = 1
    else:
        state = 0
    success = update_state(Username, Product_Name, state)
    if success:
        message["message"] = "ON"
    else:
        message["message"] = "OFF"
    return message

# A route for getting the current state of the blinds
@app.post("/schedule")
def add_schedule_html(schedule: Schedule, request: Request) -> dict:
    message = {}
    # HH:MM
    start_time = schedule.Start_Time
    end_time = schedule.End_Time
    state = schedule.State
    Username = request.cookies.get("Username")
    Product_Name = request.cookies.get("Product_Name")
    serial = return_serial(Username, Product_Name)
    success = add_schedule(start_time, end_time, state, serial)
    if success:
        message["message"] = "Schedule Added"
    else:
        message["message"] = "Schedule not added"
    return message

# Routes for the schedule for the product page to update the button
@app.get("/schedule/product")
def get_new_state(request: Request) -> dict:
    #print("inside")
    message = {}
    Username = request.cookies.get("Username")
    Product_Name = request.cookies.get("Product_Name")
    serial = return_serial(Username, Product_Name)
    # Check if the schedules and see if the blinds should be in a different state
    schedule_check(serial)
    success = state_check(serial)
    
    if success:
        message["message"] = "ON"
    else:
        message["message"] = "OFF"

    return message



# Routes for the product fetches
@app.get("/data/{serial}")
def get_json(serial:str) -> dict:
    message = {}
    # Check if the schedules and see if the blinds should be in a different state
    schedule_check(serial)
    success = state_check(serial)
    
    if success:
        message["message"] = "ON"
    else:
        message["message"] = "OFF"

    return message



if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=3000)