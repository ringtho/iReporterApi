import unittest
from api.routes import app
from tests.get_token import GetTokenTests
import json
from api import routes


class TestUserRoutes(unittest.TestCase):
    def setUp(self):
        """initialise test client"""
        self.test_client = app.test_client()

    def test_create_user(self):
        user = {
	
            "firstname": "smith",
            "lastname": "Ringtho",
            "othernames": "J",
            "email": "sringtho@gmail.com",
            "phoneNumber": "0778339655",
            "username": "sringtho1",
            "password": "sr654321"

            }
        response = self.test_client.post("/api/v1/auth/register",json=user)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        # print(data)
        self.assertEqual(data["status"], 201)
        self.assertEqual(data["data"][0]["message"], "User successfully created")
        self.assertEqual(data["data"][0]["user"]["username"], "sringtho1")
    def test_add_user_missing_username(self):
        user = {
	
            "firstname": "smith",
            "lastname": "Ringtho",
            "othernames": "J",
            "email": "sringtho@gmail.com",
            "phoneNumber": "0778339655",
            "password": "sr654321"

        }
        response = self.test_client.post("/api/v1/auth/register",json=user)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # print(data)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["Error"], "username not specified")

    def test_login(self):
        user = {
	
            "firstname": "smith",
            "lastname": "Ringtho",
            "othernames": "J",
            "email": "sringtho@gmail.com",
            "phoneNumber": "0778339655",
            "username": "sringtho",
            "password": "sr654321"

        }
        response = self.test_client.post("/api/v1/auth/register",json=user)
        self.assertEqual(response.status_code, 201)
        user_login = {
            "username": "sringtho",
            "password": "sr654321"
            }
        response=self.test_client.post("/api/v1/auth/login" ,json=user_login)
        data = json.loads(response.data)
        # print(data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["status"], 201)
        self.assertEqual(data["data"][0]["message"], "Logged in successfully")

        # def test_incorrect_login_details(self):
    #     user = {
	
    #         "firstname": "smith",
    #         "lastname": "Ringtho",
    #         "othernames": "J",
    #         "email": "sringtho@gmail.com",
    #         "phoneNumber": "0778339655",
    #         "username": "sringtho",
    #         "password": "sr654321"

    #         }
    #     response = self.test_client.post("/api/v1/auth/register",json=user)
    #     self.assertEqual(response.status_code, 201)
    #     user_login = {
    #         "username": "smith",
    #         "password": "sr654321"
    #         }
    #     response=self.test_client.post("/api/v1/auth/login" ,json=user_login)
    #     data = json.loads(response.data)
    #     print(data)
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(data["status"], 201)
    #     self.assertEqual(data["data"][0]["message"], "Logged in successfully")
