# Smart_Blinds
ECE 140B Project by Sialoi Taa, Taimur Shaikh and Christian Hendric

## Project
This project is called the "Smart Blinds" project and the purpose of this project is to create a product that will turn ON and OFF our project via remote or via server through some customization settings.

## Front End Design
When going to the site to remote access their Smart Blinds product, the user must be a registered user. They will be prompted to sign in or register. Registering requires their email, a unique username and password. After completing the registration, the user will be prompted to sign in with their email and password. A valid login will relocate the user to another page that holds all of the products under that account and an "Add Product" button that will let the user add more accounts to the account. Clicking on the add product button will create a box that will create a box that will let the user add the product's serial number and a unique product name. Pressing "Submit" at the bottom of that box will allow the user to add that product to their list of products owned. Any registered product will be listed on the welcome page of the user as a button. With that will also come a delete button that will delete that product's information from that user. Clicking on that button will show that product's serial number, a schedule feature and an On/OFF button. Clicking the On/Off button will change the state of the product from clear to opaque and vice versa. Clicking on the schedule feature will enable the user to add a schedule to that product. To be able to add a schedule, the user must put in a valid time slot and the state that they wish the product to be in. Pressing the "Submit" button will add that schedule with the desired state to that product's information page. There will also be a delete button for every time slot.
  
### Front End Design Diagram
![Front End Design](images/FED.jpg)
___
## Back End Design
In the back end design, there's a *Users* table that will hold each user's name, password, email. Next will be an *Active_Users* table that will keep track who has logged in and will use the timestamp in the MySQL table to decide when to end the session (after 900 seconds). After that will be a *Schedule* table that will hold the scheduled times for the Smart Blinds product to be turned OFF or ON and the serial number of the product. Then we have the *State* table and that will tell us the state the product is in currently. The *Owners* table will hold the user's username, the product's special name and serial number. The last table we will have is the *Unregistered* table that will hold all of the unassigned Smart Blinds products that are out on the market.  
  
In the login page, the user's input will be processed and see if we have any credentials matching what was given, if not the page will reload and the user will be prompted to put in their information again (the Users and Active_Users tables are used on this page). In the registration page, the user's input will again be processed and if their input is unique then the user will now be registered. After getting past these two pages, there's two more pages left (the Users table is used on this page). Next is the home page for the user and all of their products listed under them. This page will be accessing the Active_Users, Owners and Unregistered tables depending on the user's actions. Adding a product under that account will access the Unregistered and Owners table to take the serial number off of the Unregistered table and place it under the username and product nickname inside the Owners table. Deleting a product from the account on this page will do the reverse, take the serial number from the Owners table, delete that row and add the serial number to the Unregistered table again. The Active_Users table will be accessed every 10 seconds to check to see if the session_ID has expired. Lastly, the features page is product specific, meaning that these are the features of a singular Smart Blinds product. This page will have access to the State, Schedule and Active_Users table. Every 10 seconds, the Active_Users table will be asked if the session_ID is expired yet. The user has the option of turning the product ON or OFF through the ON/OFF button and will subsequently change the State table. The last table to be interacted with is the Schedule table that will store all of the users' specific settings for timed actions. These scheduled events override current states and will change the State table as a consequence as well. 
  
### Back End Design Diagram
![Back End Design](images/BED.jpg)


# NOTES FOR NEXT TIME
* You finished the landing, login, and registration page.
* You're finishing the HTML and JS integration for the home page.
* You need to add the setInterval function to keep checking the cookies
* After finishing up the Home page, get started on the Product page that will hold the customization for each individual product.
* The customization page will connect and change the Schedule and State tables accordingly and possibly add multiprocessing that will run on the server to follow the schedules.
* Look at a way for a controller to stay connected to the internet and keep getting server updates for IoT.

* 5/24/23, 4:46 AM, 1018 lines