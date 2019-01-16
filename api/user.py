from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

count = 1

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
        self.password = generate_password_hash(kwargs['password'])
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
            "isAdmin": self.isAdmin
        }
        return format

    def user_data(self, data):
        return User(firstname = data['firstname'], lastname = data['lastname'],
        othernames = data['othernames'], email = data['email'], phoneNumber = data['phoneNumber'],
         username = data['username'], password = data['password'])
         
