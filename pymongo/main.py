from pymongo import MongoClient
from datetime import datetime
import sys

#client = MongoClient("mongodb://localhost:27017/")
pwd = sys.argv[1]
client = MongoClient("mongodb+srv://admin:" + pwd + "@cluster0-mgsjh.mongodb.net/test?retryWrites=true&w=majority")
db = client["Maria"]
clients = db["Clients"]
clients.drop()
newclient1 = {
    "name": "Hans Meiser", 
    "description": "Lorem ipsum dolor", 
    "tags": ["heart", "lung"], 
    "dateOfBirth": datetime(1963, 11, 20)
    }
clients.insert_one(newclient1)

newclient2 = {
    "name": "Mike Mustermann", 
    "description": "Lorem ipsum dolor", 
    "tags": [ "lung", "liver"], 
    "dateOfBirth": datetime(1975, 1, 29)
    }
clients.insert_one(newclient2)

for c in clients.find(): #{"name": {"$regex": u"Hans"}}):
    print(c["name"])