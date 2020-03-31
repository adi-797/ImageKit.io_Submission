# ImageKit.io Assignment
This repository contains the submission for the ImageKit.io recruitment process ( Position - Software Engineer ).

Problem Statement:

Create a basic user registration page - a user enters the information and it is stored in a database. However, there are certain conditions that should be kept in mind while developing the front end and the backend for this,

1. The HTML page should take only 3 user inputs - Name, email, and password. No need
to go fancy with the CSS. Just a plain simple form would do.
2. If someone from the same IP address attempts to register more than 3 times in a day,
they should be presented with a captcha (Google Recaptcha). The captcha should be
validated for all subsequent attempts to register for that IP address.
3. If everything in the input is fine, then the user details should be stored in a Mongo
database.

----

# Solution

Technology Stack:
Python 3 - Django, MongoDB ( pymongo )

Python Library Requirements:
Django==3.0.4, dnspython==1.16.0, pymongo==3.10.1

Features:
1) Form fields validations using HTML.
2) IP address validation using Django backend.
3) The permanent data is stored in a MongoDB which is hosted online on cloud.mongodb.com and is accessed using pymongo. A script is provided for accessing the data on MongoDB and storing it locally in a csv file. Location: ..\checkData.py

How to execute:

1) Make sure you have Python 3 installed and all Library requirements have been met.

For installing the required libraries,
Open your command shell and execute the command-> pip install django dnspython pymongo

2) Open your command shell and navigate into ..\ImageKitioAssignment
2) Execute the command-> python manage.py runserver
3) Open local host (127.0.0.1:8000) in any broswer to access the web page.

Note: Comments are provided in the scripts for better understanding of the logic.
