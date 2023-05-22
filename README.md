# Smart_Blinds
ECE 140B Project by Sialoi Taa, Taimur Shaikh and Christian Hendric

## Project
This project is called the "Smart Blinds" project and the purpose of this project is to create a product that will turn ON and OFF our project via remote or via server through some customization settings.

## Front End Design
When going to the site to remote access their Smart Blinds product, the user must be a registered user. They will be prompted to sign in or register. Registering requires their email, a unique username and password. After completing the registration, the user will be prompted to sign in with their email and password. A valid login will relocate the user to another page that holds all of the products under that account and an "Add Product" button that will let the user add more accounts to the account. Clicking on the add product button will create a box that will create a box that will let the user add the product's serial number and a unique product name. Pressing "Submit" at the bottom of that box will allow the user to add that product to their list of products owned. Any registered product will be listed on the welcome page of the user as a button. Clicking on that button will show that product's serial number, a schedule feature and an On/OFF button. Clicking the On/Off button will change the state of the product from clear to opaque and vice versa. Clicking on the schedule feature will enable the user to 
  
![Front End Design](/Smart_Blinds/Smart_Blinds/images/Front_End_Design.jpg)
___
## Back End Design
In the back end design, there's a user's table that will hold each user's name, password, email and all products under their name. Next will be an active user's table that will keep track who has logged in and will use the multiprocessing library to create a thread for each person and log them out when the time comes (10 mins) or have the table to . After that will be a Schedule table that will hold the scheduled times for the Smart Blinds product to be turned OFF. 
  
![Back End Design](/Smart_Blinds/Smart_Blinds/images/Back_End_Design.jpg)


