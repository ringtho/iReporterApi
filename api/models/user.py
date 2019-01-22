from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, abort
from api.db.db_connect import Database
from api.validator import Validator

cursor = Database().cursor

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

    def __init__(self, request):
        validator = Validator(request)
        if validator.validate_user_data():
            pass
        else:
            raise Exception(validator.error)

    def create_user(self,firstname, lastname, othernames, username, phoneNumber, password, email, role):
        global cursor
        create_user= """
        INSERT INTO users (firstname, lastname, othernames, username, phoneNumber, password, email,role) 
        VALUES('{}','{}','{}','{}','{}','{}','{}','{}')""".format(firstname, 
        lastname, othernames, username, phoneNumber, password, email,role)
        return cursor.execute(create_user)
    

def get_user(username, password):

    for user in users:
        if user["username"] == username and check_password_hash(user["password"], password):
            return user




         
