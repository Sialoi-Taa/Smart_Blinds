'''
This file only creates a new database and empty tables at the start of 
'''

# Add the necessary imports
import mysql.connector as mysql
from dotenv import load_dotenv
import os
import datetime

# Read Database connection variables
''' Environment Variables '''
load_dotenv("credentials.env")
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

# Connect to the db and create a cursor object
db = mysql.connect(user=db_user, password=db_pass, host=db_host)
cursor = db.cursor()

# Creates a DB that doesn't exist yet
cursor.execute("CREATE DATABASE if not exists Smart_Blinds;")
cursor.execute("USE Smart_Blinds;")

# Create a Menu_Items table
cursor.execute("drop table if exists Sensors;")
try:
   cursor.execute("""
   CREATE TABLE if not exists Sensors (
       id                  INTEGER  AUTO_INCREMENT PRIMARY KEY,
       name                VARCHAR(25) NOT NULL,  
       sensor_value        DECIMAL(10, 2) NOT NULL,
       created_at          TIMESTAMP,
       updated             TIMESTAMP
   );
 """)
   
   # Initiates the starting rows to be changed during runtime
   query = "INSERT INTO Sensors (name, sensor_value, created_at, updated) VALUES (%s, %s, %s, %s)"
   values = [  ('accelx',
               0.00, 
               datetime.datetime.now(),
               datetime.datetime.now()),
               ('gyrox',
               0.00, 
               datetime.datetime.now(),
               datetime.datetime.now()),

               ('accely',
               0.00, 
               datetime.datetime.now(),
               datetime.datetime.now()),
               ('gyroy',
               0.00, 
               datetime.datetime.now(),
               datetime.datetime.now()),

               ('accelz',
               0.00, 
               datetime.datetime.now(),
               datetime.datetime.now()),
               ('gyroz',
               0.00, 
               datetime.datetime.now(),
               datetime.datetime.now()),
               
               ('infra',
               0.00, 
               datetime.datetime.now(),
               datetime.datetime.now()),
               ('ultra',
               0.00, 
               datetime.datetime.now(),
               datetime.datetime.now()),
               ('photo',
               0.00, 
               datetime.datetime.now(),
               datetime.datetime.now())]
   cursor.executemany(query, values)
   
except RuntimeError as err:
   print("runtime error: {0}".format(err))

# Commits the changes to the DB inside our system for persistent data
db.commit()
db.close()