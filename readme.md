# Maria
This project is there to help to work with clients in the health facility.
The users goal is to help people with there health with consultancies.
This app will help to register costumers and to track consultancies.

## Installation
In order to run Maria you have to install tinydb and PyQt5 if not already installed.    
Run the following command in a terminal.  
```console
user@machine:/path$ pip3 install --user tinydb
``` 

Also PyQt5 is needed to be installed.  
```console
user@machine:/path$ pip3 install --user PyQt5
``` 

To install the application you have to clone the repository.  
```console
user@machine:/path$ git clone https://github.com/CrowdWare/maria.git
``` 

## Run the app
In order to run the app change into the directory maria and run the following command.
```console
user@machine:/path$ cd maria
user@machine:/path$ python3 main.py
``` 

## Backup
To backup the data create a copy on a regular base of the file **maria.json**.  
This file contains the database.

## Status
The application is in a very basic state. You are only able to enter customers and edit their notes.  
More to come...