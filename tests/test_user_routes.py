import unittest
from api.routes import app
from tests.get_token import GetTokenTests
import json
from api import routes


class TestUserRoutes(unittest.TestCase):
    def setUp(self):
        """initialise test client"""
        self.test_client = app.test_client()
        self.user = {
	
            "firstname": "smith",
            "lastname": "Ringtho",
            "othernames": "J",
            "email": "sringtho@gmail.com",
            "phoneNumber": "+256778339655",
            "username": "sringtho",
            "password": "Sr654321"

        }
        self.user_name={
            "firstname": "smith",
            "lastname": "Ringtho",
            "othernames": "J",
            "email": "sringtho@gmail.com",
            "phoneNumber": "+256778339655",
            "password": "Sr654321"
        }
        self.user_login = {
            "username": "sringtho",
            "password": "Sr654321"
        }

    def test_create_user(self):
        response = self.test_client.post("/api/v1/auth/register",json=self.user)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(data["status"], 201)
        self.assertEqual(data["data"][0]["message"], "User successfully created")
        self.assertEqual(data["data"][0]["user"]["username"], "sringtho")

    def test_add_user_missing_username(self):
        response = self.test_client.post("/api/v1/auth/register",json=self.user_name)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        # print(data)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["Error"], "username not specified")

    def test_login(self):
      
        response = self.test_client.post("/api/v1/auth/register",json=self.user)
        self.assertEqual(response.status_code, 201)
        response=self.test_client.post("/api/v1/auth/login" ,json=self.user_login)
        data = json.loads(response.data)
        # print(data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["status"], 201)
        self.assertEqual(data["data"][0]["message"], "Logged in successfully")

    def test_incorrect_login_details(self):
        response = self.test_client.post("/api/v1/auth/register",json=self.user)
        self.assertEqual(response.status_code, 201)
        user_login = {
            "username": "smith",
            "password": "Sr654321"
            }
        response=self.test_client.post("/api/v1/auth/login" ,json=user_login)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["Error"], "Invalid Username or Password")

    def test_user_missing_login_password(self):
        response = self.test_client.post("/api/v1/auth/register",json=self.user)
        self.assertEqual(response.status_code, 201)
        login = {
            "username":"sringtho1"
        }
        response=self.test_client.post("/api/v1/auth/login" ,json=login)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["Error"], "password not specified")

    def test_user_missing_login_username(self):
        response = self.test_client.post("/api/v1/auth/register",json=self.user)
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
