from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, abort
from api.db.db_connect import Database
from api.validator import Validator
import hashlib

cursor = Database().cursor

count = 1

class User:

    def create_user(self,firstname, lastname, othernames, username, phoneNumber, password, email, isAdmin):
        # cursor = Database().cursor
        cur = Database().cur
        create_user= """
        INSERT INTO users (firstname, lastname, othernames, username, phoneNumber, password, email,isAdmin) 
        VALUES('{}','{}','{}','{}','{}','{}','{}','{}')""".format(firstname, 
        lastname, othernames, username, phoneNumber, password, email,isAdmin)
        return cur.execute(create_user)
    

    def get_user(self, username, password):
        query = f"SELECT username,password,id,isAdmin FROM users WHERE username='{username}'"
        print(query)
        cursor.execute(query)
        user = cursor.fetchone()
        if check_password_hash(user["password"], password):
            return user

    def get_all_users(self):
        query = f"SELECT * FROM users"
        cursor.execute(query)
        users = cursor.fetchall()
        return users

    def delete_particular_user(self, user_id):
        cur = Database().cur
        query = f"DELETE FROM users WHERE id={user_id}"
        cur.execute(query)
        rows = cur.rowcount
        return rows


        
