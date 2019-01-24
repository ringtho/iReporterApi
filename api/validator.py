import re
from api.db.db_connect import Database

cursor = Database().cursor

class Validator:
    def __init__(self, request):
        self.request = request

    def redflag_is_valid(self):
        try:
            redflag = self.request.get_json()
            self.ensure_no_empty_fields(redflag)
            self.ensure_valid_data_types(redflag)
            return True
        except Exception as e:
            self.error = str(e)
            return False

    def ensure_no_empty_fields(self, redflag):
        # assert 'createdOn' in redflag, 'createdOn field not specified.'
        # assert 'createdBy' in redflag, 'createdBy field not specified.'
        assert 'incident_type' in redflag, 'incident type field not specified.'
        assert 'location' in redflag, 'location field not specified.'
        assert 'images' in redflag, 'images field not specified.'
        assert 'videos' in redflag, 'videos field not specified.'
        assert 'comment' in redflag, 'comment field not specified.'

    def ensure_valid_data_types(self, redflag):
        # assert isinstance(redflag['createdBy'], int), (
        # 'createdBy should be an integer')
        assert isinstance(redflag["location"], str), (
        "Location should be a string containing latitude and longitude coordinates!")
        assert isinstance(redflag["images"], str), ("Images must be of string type")
        assert isinstance(redflag["videos"], str), ("Videos must be of string type")

    def valid_location_for_edit(self):
        try:
            redflag = self.request.get_json()
            self.ensure_valid_location_for_edit(redflag)
            return True
        except Exception as e:
            self.error = str(e)
            return False

    def ensure_valid_location_for_edit(self, redflag):
        assert isinstance(redflag["location"], str), (
        "Location should be a string containing latitude and longitude coordinates!")
     

    def validate_user_data(self):
        try:
            user_data = self.request.get_json()
            assert isinstance(user_data, dict),'Ensure to enter registration details in json format'
            self.ensure_no_empty_fields_user(user_data)
            self.ensure_items_correct_datatype(user_data)
            self.validate_email_address(user_data["email"])
            self.validate_password(user_data["password"])
            self.validate_phone_number(user_data["phoneNumber"])
            self.check_if_user_exists_already(user_data["username"], user_data["email"])
            return True
        except Exception as e:
            self.error = str(e)
            return False

    def ensure_no_empty_fields_user(self, user_data):
        assert 'firstname' in user_data, 'Firstname not specified'
        assert 'lastname' in user_data, 'lastname not specified'
        assert 'firstname' in user_data, 'firstname not specified'
        assert 'email' in user_data, 'Please provide an email'
        assert 'phoneNumber' in user_data, 'phoneNumber not specified'
        assert 'username' in user_data, 'username not specified'
        assert 'password' in user_data, 'password not specified'

    def ensure_items_correct_datatype(self, user_data):
        assert isinstance(user_data["phoneNumber"], str), 'phoneNumber should be a string!'
        assert isinstance(user_data["email"], str), 'Email should be a string!!'
        assert isinstance(user_data["username"], str), 'Username should be a string'
        assert isinstance(user_data["firstname"], str), 'Firstname should be a string!!'
        assert isinstance(user_data["lastname"], str), 'Lastname should be string'
        assert isinstance(user_data["othernames"], str), 'Othernames should be a string'

    
    def validate_login_data(self):
        try:
            user_data = self.request.get_json()
            self.ensure_no_empty_fields_login(user_data)
            return True
        except Exception as e:
            self.error = str(e)
            return False


    def ensure_no_empty_fields_login(self,user_data):
        assert 'username' in user_data, 'username not specified'
        assert 'password' in user_data, 'password not specified'
        assert isinstance(user_data, dict),'Ensure to enter login details in json format'

    def validate_email_address(self, email):
        assert isinstance(email, str), 'Email address must be a string!'
        pattern = re.compile(r'[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]{2,3}((\.[a-zA-Z]{2,3})+)?$')
        assert pattern.match(email.strip()), 'Invalid Email Address!'

    def validate_password(self, password):
        assert isinstance(password, str), 'Password must be a string!'
        check_password = {
        'a-z': str.islower, 
        'A-Z': str.isupper, 
        '0-9': str.isdigit
        }
        for letter in password:
            for key, value in check_password.items():
                if value(letter):
                    del check_password[key]
                    break 
        password_is_valid = len(check_password) == 0 and 8 <= len(password) <= 12
        error_message = (
            'Password must contain atleast one lowercase letter, one uppercase letter,'
            ' a digit and be 8 to 12 characters long!'
        )
        assert password_is_valid, error_message  

    def validate_phone_number(self, phone):
        assert isinstance(phone, str), 'Telephone contact must be a string!'
        telephone_pattern = re.compile(r'\+[0-9]{12}$')
        assert telephone_pattern.match(phone.strip()), 'Telephone contact is invalid!'
    
    def check_if_user_exists_already(self, username, email):
        global cursor
        query = """SELECT username FROM users WHERE username='{}'""".format(username)
        query1 = """SELECT email FROM users WHERE email='{}'""".format(email)
        cursor.execute(query)

        if cursor.fetchall():
            raise Exception(f'{username} already exists')
        
        cursor.execute(query1)
        if cursor.fetchall():    
            raise Exception(f'{email} already in the system')
       




        