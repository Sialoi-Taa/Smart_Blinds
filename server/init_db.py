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
# <----------------------------------------------------------->
# Creating Tables
try:
    # Create a Users table
    cursor.execute("""
    CREATE TABLE if not exists Users (
        id                   INTEGER  AUTO_INCREMENT PRIMARY KEY,
        Username             VARCHAR(25) NOT NULL,  
        Password             VARCHAR(100) NOT NULL,  
        Email                VARCHAR(50) NOT NULL
    );
    """)
    # Create an Active_Users table
    cursor.execute("""
    CREATE TABLE if not exists Active_Users (
        id                   INTEGER  AUTO_INCREMENT PRIMARY KEY,
        Username             VARCHAR(25) NOT NULL,
        Cookie               VARCHAR(100) NOT NULL,
        created_at           TIMESTAMP
    );
    """)
    # Create a Schedule table
    cursor.execute("""
    CREATE TABLE if not exists Schedule (
        id                   INTEGER  AUTO_INCREMENT PRIMARY KEY,
        Serial               VARCHAR(25) NOT NULL,  
        Start_Time           VARCHAR(10) NOT NULL,  
        End_Time             VARCHAR(10) NOT NULL,  
        State                INTEGER(1) NOT NULL
    );
    """)
    # Create a State table
    cursor.execute("""
    CREATE TABLE if not exists State (
        id                   INTEGER  AUTO_INCREMENT PRIMARY KEY,
        Serial               VARCHAR(25) NOT NULL, 
        State                INTEGER(1) NOT NULL
    );
    """)
    # Set the state of the prototype
    cursor.execute("INSERT INTO State (Serial, State) VALUES (%s, %s)", ("PROTOTYPE", "0"))
    # Create an Owners table
    cursor.execute("""
    CREATE TABLE if not exists Owners (
        id                   INTEGER  AUTO_INCREMENT PRIMARY KEY,
        Username             VARCHAR(25) NOT NULL,  
        Serial               VARCHAR(25) NOT NULL,   
        Product_Name         VARCHAR(50) NOT NULL
    );
    """)
    # Create an Unregistered table
    cursor.execute("""
    CREATE TABLE if not exists Unregistered (
        id                   INTEGER  AUTO_INCREMENT PRIMARY KEY,
        Serial               VARCHAR(25) NOT NULL
    );
    """)
    # Place the prototype
    cursor.execute("INSERT INTO Unregistered (Serial) VALUES (%s)", ("PROTOTYPE"))
except RuntimeError as err:
   print("runtime error: {0}".format(err))

# Commits the changes to the DB inside our system for persistent data
db.commit()
db.close()