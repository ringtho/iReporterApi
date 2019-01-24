from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, abort
from api.db.db_connect import Database
from api.validator import Validator
import hashlib

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

    def create_user(self,firstname, lastname, othernames, username, phoneNumber, password, email, isAdmin):
        global cursor
        create_user= """
        INSERT INTO users (firstname, lastname, othernames, username, phoneNumber, password, email,isAdmin) 
        VALUES('{}','{}','{}','{}','{}','{}','{}','{}')""".format(firstname, 
        lastname, othernames, username, phoneNumber, password, email,isAdmin)
        return cursor.execute(create_user)
    

    def get_user(self, username, password):
        query = f"SELECT username,password,id,isAdmin FROM users WHERE username='{username}'"
        print(query)
        cursor.execute(query)
        user = cursor.fetchone()
        if check_password_hash(user["password"], password):
            return user


        
