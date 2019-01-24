import unittest
from api.views.routes import app
from tests.get_token import GetTokenTests
import json
from api.db.db_connect import Database
from api.models.user import User
from api.views import routes

# cursor = Database().cursor


class TestUserRoutes(unittest.TestCase):
    def setUp(self):
        """initialise test client"""
        self.test_client = app.test_client()
        self.db = Database()
        # self.db.create_tables()

        self.user = {
	
            "firstname": "Mark",
            "lastname": "Henry",
            "othernames": "J",
            "email": "mark@gmail.com",
            "phoneNumber": "+256778339655",
            "username": "mark",
            "password": "Sr654321"

        }


        self.user2 = {
	
            "firstname": "Mark",
            "lastname": "Henry",
            "othernames": "J",
            "email": "sringtho@gmail.com",
            "phoneNumber": "+256778339655",
            "username": "sringtho",
            "password": "Sr654321"

        }

        self.username = {
	
            "firstname": "Mark",
            "lastname": "Henry",
            "othernames": "J",
            "email": "mark@gmail.com",
            "phoneNumber": "+256778339655",
            "password": "Sr654321"

        }

        self.user_login = {
            "username": "mark",
            "password": "Sr654321"
        }

       

    def tearDown(self):
        self.db.empty_tables()
        # self.db.create_users_table()
        # self.db.create_redflags_table()
        # self.db.create_interventions_table()
       
    def test_create_user(self):
        response = self.test_client.post("/api/v1/auth/signup",json=self.user)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(data["status"], 201)
        self.assertEqual(data["data"][0]["message"], "User successfully created")


    def test_add_user_missing_username(self):
        response = self.test_client.post("/api/v1/auth/signup",json=self.username)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        # print(data)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["Error"], "username not specified")

    def test_login(self):
        response = self.test_client.post("/api/v1/auth/signup",json=self.user)
        self.assertEqual(response.status_code, 201)
        response=self.test_client.post("/api/v1/auth/login" ,json=self.user_login)
        data = json.loads(response.data)
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)


    def test_incorrect_login_details(self):
        response = self.test_client.post("/api/v1/auth/signup",json=self.user)
        self.assertEqual(response.status_code, 201)
        user_login = {
            "username": "mark",
            "password": "Sr65431"
            }
        response=self.test_client.post("/api/v1/auth/login" ,json=user_login)
        data = json.loads(response.data)
        # print(data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["Error"], "Invalid Username or Password")

    def test_user_missing_login_password(self):
        response = self.test_client.post("/api/v1/auth/signup",json=self.user)
        self.assertEqual(response.status_code, 201)
        login = {
            "username":"sringtho1"
        }
        response=self.test_client.post("/api/v1/auth/login" ,json=login)
        data = json.loads(response.data)
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["Error"], "password not specified")

    def test_user_missing_login_username(self):
        response = self.test_client.post("/api/v1/auth/signup",json=self.user)
        self.assertEqual(response.status_code, 201)
        login = {
            "password":"sringtho1"
        }
        response=self.test_client.post("/api/v1/auth/login" ,json=login)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["Error"], "username not specified")

    def test_username_already_exists(self):
        user2 = {"firstname": "smith","lastname": "Ringtho","othernames": "J",
            "email": "sringtho@yahoo.com","phoneNumber": "+256778339655",
            "username": "mark","password": "Sr654321"}
        response = self.test_client.post("/api/v1/auth/signup", json=self.user)
        response = self.test_client.post("/api/v1/auth/signup", json=user2)
        data = json.loads(response.data)
        # print(data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(data["Error"], "mark already exists")
        self.assertEqual(data["status"], 400)

    def test_email_already_exist(self):
        user2 = {"firstname": "smith","lastname": "Ringtho","othernames": "J",
            "email": "mark@gmail.com","phoneNumber": "+256778339655",
            "username": "smith","password": "Sr654321"}
        response = self.test_client.post("/api/v1/auth/signup", json=self.user)
        response = self.test_client.post("/api/v1/auth/signup", json=user2)
        data = json.loads(response.data)
        # print(data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(data["Error"], "mark@gmail.com already in the system")
        self.assertEqual(data["status"], 400)
    
    # def test_get_users(self):
    #     getter = GetTokenTests()
    #     token = getter.get_admin_token()
    #     headers={"Authorization":"Bearer " + token}
    #     response = self.test_client.post("/api/v1/auth/signup", json=self.user)
    #     response = self.test_client.post("/api/v1/auth/signup", json=self.user2)
    #     self.assertEqual(response.status_code, 201)
    #     res = self.test_client.get("/api/v1/auth/users", headers=headers)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["status"], 200)
    #     self.assertEqual(data["data"][1]["firstname"], "smith")

 
if __name__ == '__main__':
    unittest.main()
    
