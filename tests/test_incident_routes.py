import unittest
from api.views.routes import app
from tests.get_token import GetTokenTests
import json
from api.views import routes

class TestRedFlags(unittest.TestCase):
    def setUp(self):
        """initialise test client"""
        self.test_client = app.test_client()
        self.incident = {
       
        "createdBy": 1, 
        "types":"redflag", 
        "location":{"Latitude": "0.321", "Longitude": "35.145"}, 
        "status": "rejected", 
        "images": ["image.jpg", "image2.jpg"],
        "videos": ["videos.org","video2.org"], 
        "comment": "my name is"
        }
        self.incidents = { "createdBy": 1, "types":"redflag", 
        "location":{"Latitude": "0.3245", "Longitude": "40.687"}, 
        "status": "accepted", "images": ["image.jpg","image2"], 
        "videos": ["videos.mp4","smith.mkv"], 
        "comment": "The most corrupt official ever"}

    def tearDown(self):
        response = self.test_client.get('/api/v1/red-flags',
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)))
        data = json.loads(response.data)
        if 'data' in data:
            for redflag in data['data']:
                self.test_client.delete('/api/v1/red-flags/{}'.format(redflag['id']), 
                headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)),)

    def test_hello_world(self):
        response = self.test_client.get("/")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(data["message"], "Hello World, it's Smith!!")
        self.assertEqual(data["status"], 200)

    def test_empty_database(self):
        response = self.test_client.get("/api/v1/red-flags", headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)))
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn(data["message"], "There are no red flags in the database")

    def test_create_redflag(self):
        response = self.test_client.post("/api/v1/red-flags", 
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)),
         content_type='application/json',json=self.incident)
        data =json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(data["data"][0]["message"], "red flag record created.")
        self.assertEqual(data["data"][0]["id"], 1)
        self.assertEqual(data["status"],201)

    def test_get_all_redflags(self):
        response = self.test_client.post("/api/v1/red-flags",headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)), json=self.incidents)
        response1 = self.test_client.post("/api/v1/red-flags",headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)), json=self.incident)
        self.assertEqual(response.status_code, 201)
        self.assertIn(response.json["data"][0]["message"], "red flag record created.")
        self.assertIn(response1.json["data"][0]["message"], "red flag record created.")
        res = self.test_client.get("/api/v1/red-flags",headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)),)
        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("accepted", data["data"][0]["status"])
        self.assertIn("rejected", data["data"][1]["status"])
        self.assertEqual(data["data"][0]["images"], ["image.jpg","image2"])
        self.assertEqual(len(data), 2)

    def test_get_single_redflag(self):
        response = self.test_client.post("/api/v1/red-flags",
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)), json=self.incident)
        self.assertEqual(response.status_code, 201)
        self.assertIn(response.json["data"][0]["message"], "red flag record created.")
        res = self.test_client.get("/api/v1/red-flags/{}".format(response.json["data"][0]["id"]),
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)))
        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code, 200)
        self.assertIn(data["data"][0]["status"], "rejected")
        self.assertIn(data["data"][0]["location"]["Latitude"], "0.321" )

    def test_edit_location(self):
        response = self.test_client.post("/api/v1/red-flags",
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)), json=self.incident)
        self.assertEqual(response.status_code, 201)
        location = {"location": {"Latitude": "5.056", "Longitude":"56.234"}}
        res = self.test_client.patch("/api/v1/red-flags/{}/location"
        .format(response.json["data"][0]["id"]) ,
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)),json=location)
        data = json.loads(res.data)
        # print(data)
        self.assertIn(data["data"][0]["message"], "Updated red-flag record's location")
        self.assertEqual(res.status_code, 200)
        
    def test_edit_comment(self):
        response = self.test_client.post("/api/v1/red-flags",
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)), json=self.incident)
        self.assertEqual(response.status_code, 201)
        comment = {"comment": "Museveni is so corrupt","location": {"Latitude": "5.056", "Longitude":"56.234"}}
        res = self.test_client.patch("/api/v1/red-flags/{}/comment".format(response.json["data"][0]["id"]),
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)),json=comment)
        data =json.loads(res.data)
        # print(data)
        self.assertIn(data["data"][0]["message"], "Updated red-flag record's comment")
        self.assertEqual(res.status_code, 200)
      
    def test_delete_redflag(self):
        response = self.test_client.post("/api/v1/red-flags",
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)), json=self.incident)
        self.assertEqual(response.status_code, 201)
        res = self.test_client.delete("/api/v1/red-flags/{}".format(response.json["data"][0]["id"]),
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)))
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["data"][0]["message"], "red-flag record has been deleted")
        self.assertEqual(data["status"], 200)

    def test_createdBy_string(self):
        incident = { "createdBy": "user", "types":"redflag", "location":{"Latitude": "5.056", "Longitude":"56.234"}, 
        "status": "accepted", "images": ["image.jpg","image2"], "videos": ["videos.mp4","smith.mkv"], 
        "comment": "The most corrupt official ever"}
        response = self.test_client.post("/api/v1/red-flags",content_type='application/json',
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)), json=incident)
        data = json.loads(response.data)
        # print(data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["Error"], "createdBy should be an integer")
       
    def test_delete_nonexistent_object(self):
        response = self.test_client.delete("/api/v1/red-flags/2",
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)))
        data = json.loads(response.data)
        # print(data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["status"], 404)
        self.assertIn("The red flag record with id 2 doesnt exist", data["Error"])

    def test_error_patch_invalid_id(self):
        response = self.test_client.post("/api/v1/red-flags",
         headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)), json=self.incident)
        self.assertEqual(response.status_code, 201)
        location = {"location": {"Latitude": "5.056", "Longitude":"56.234"}}
        response = self.test_client.patch("/api/v1/red-flags/2/location" ,
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)),json=location)
        data = json.loads(response.data)
        # print(data)
        self.assertEqual(data["status"], 404)
        self.assertIn("Non existent redflag", data["Error"])

    def test_error_patch_invalid_query_name(self):
        response = self.test_client.post("/api/v1/red-flags",
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)), json=self.incident)
        self.assertEqual(response.status_code, 201)
        location = {"location": {"Latitude": "5.056", "Longitude":"56.234"}}
        response = self.test_client.patch("/api/v1/red-flags/{}/locations"
        .format(response.json["data"][0]["id"]),
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)), json=location)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["status"], 404)
        self.assertIn("The url you provided doesnt exist", data["message"])

    def test_error_get_nonexistent_redflag(self):
        response = self.test_client.post("/api/v1/red-flags",
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)), json=self.incident)
        self.assertEqual(response.status_code, 201)
        response = self.test_client.get("/api/v1/red-flags/4",
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["status"], 404)
        self.assertIn("A redflag with an id of 4 doesnt exist",data["Error"])

    def test_error_page_not_found(self):
        response = self.test_client.post("/abc",
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["Issue"], "You have entered an unknown URL.")

    def test_method_not_allowed(self):
        response = self.test_client.patch("/api/v1/red-flags",
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)),)
        self.assertEqual(response.status_code, 405)
        data = json.loads(response.data)
        self.assertEqual(data["Error"],"Please check to ensure to check that your" 
        " calling the right method!!")

    def test_invalid_token(self):
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dWQiOjbSI6InNyaW5ndGhvMSIsImV4cCI6MTU0Nzg3NTY0NiwiYWRtIjowfQ._Gw1tIGhVCbk90BDsKnWu6tsiZ2L9FJ0OCecUWgVGJM"
        response = self.test_client.post("/api/v1/red-flags", 
        headers=dict(Authorization='Bearer '+ token),content_type='application/json',json=self.incident)
        data =json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["status"], 401)
        self.assertEqual(data["Error"], "Invalid token. Please provide a valid token")

    def test_invalid_token_used(self):
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjEsInVubSI6InNyaW5ndGhvMSIsImV4cCI6MTU0Nzg3NTY0NiwiYWRtIjowfQ._Gw1tIGhVCbk90BDsKnWu6tsiZ2L9FJ0OCecUWgVGJM"
        response = self.test_client.post("/api/v1/red-flags", 
        headers=dict(Authorization='Bearer '+ token),content_type='application/json',json=self.incident)
        data =json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["status"], 401)
        self.assertEqual(data["Error"], "Token has expired!!")


if __name__ == '__main__':
    unittest.main()