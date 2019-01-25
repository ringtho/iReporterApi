from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, abort
from api.db.db_connect import Database
from api.validator import Validator
import hashlib

# cursor = Database().get_cursor()

count = 1

class User:

    def create_user(self,firstname, lastname, othernames, username, phoneNumber, password, email, isAdmin):
        cursor = Database().get_cursor()
        create_user= """
        INSERT INTO users (firstname, lastname, othernames, username, phoneNumber, password, email,isAdmin) 
        VALUES('{}','{}','{}','{}','{}','{}','{}','{}')""".format(firstname, 
        lastname, othernames, username, phoneNumber, password, email,isAdmin)
        return cursor.execute(create_user)
    

    def get_user(self, username, password):
        cursor = Database().get_cursor()
        query = f"SELECT username,password,id,isAdmin FROM users WHERE username='{username}'"
        print(query)
        cursor.execute(query)
        user = cursor.fetchone()
        if check_password_hash(user["password"], password):
            return user

    def get_all_users(self):
        cursor = Database().get_cursor()
        query = f"SELECT firstname,email, id, lastname,username,phoneNumber, isAdmin FROM users"
        cursor.execute(query)
        users = cursor.fetchall()
        return users

    def get_particular_user(self, user_id):
        cursor = Database().get_cursor()
        query = f"SELECT firstname,email, id, lastname,username,phoneNumber, isAdmin FROM users WHERE id={user_id}"
        cursor.execute(query)
        user = cursor.fetchone()
        return user

    def delete_particular_user(self, user_id):
        cursor = Database().get_cursor()
        query = f"DELETE FROM users WHERE id={user_id}"
        cursor.execute(query)
        rows = cursor.rowcount
        return rows

    def get_id_signup(self):
        cursor = Database().get_cursor()
        query = "SELECT id FROM users ORDER BY id DESC"
        cursor.execute(query)
        user_id = cursor.fetchone()["id"]
        return user_id



        
