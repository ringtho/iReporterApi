from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, abort

count = 1

 
admin = {
    "id":0,
	"firstname": "smith",
	"lastname": "Ringtho",
	"othernames": "J",
	"email": "admin@yahoo.com",
	"phoneNumber": "+256778339655",
	"username": "admin",
	"password": "pbkdf2:sha256:50000$4RVd9ECa$57dc0f5212e7e5f9c5610a9af385c73fc54b35c27ed1f0bdad6f29ec5791282b",
    "isAdmin": 1,
    "registered": "Sun, 20 Jan 2019 21:08:15 GMT",

}   
users = [admin]

class User:

    def __init__(self, **kwargs):
        global count
        admin = 0
        self.id = count
        self.firstname = kwargs['firstname']
        self.lastname = kwargs['lastname']
        self.othernames = kwargs['othernames']
        self.email = kwargs['email']
        self.phoneNumber = kwargs['phoneNumber']
        self.username = kwargs['username']
        self.registered = datetime.today()
        self.isAdmin = admin
        self.password = kwargs['password']
        count+=1


    def json_format(self):
        format = {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "othernames": self.othernames,
            "email": self.email,
            "phoneNumber": self.phoneNumber,
            "username": self.username,
            "registered": self.registered,
            "isAdmin": self.isAdmin,
            "password": self.password
        }
        return format

def get_user(username, password):

    for user in users:
        if user["username"] == username and check_password_hash(user["password"], password):
            return user




         
