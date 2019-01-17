import unittest
from api.routes import app
from tests.get_token import GetTokenTests
import json
from api import routes

class TestRedFlags(unittest.TestCase):
    def setUp(self):
        """initialise test client"""
        self.test_client = app.test_client()
        self.incident = {
       
        "createdBy": 1, 
        "types":"redflag", 
        "location":"kampala", 
        "status": "rejected", 
        "images": "image.jpg", 
        "videos": "videos.org", 
        "comment": "my name is"
        }
        self.incidents = { "createdBy": 1, "types":"redflag", "location":"Arua", 
        "status": "accepted", "images": ["image.jpg","image2"], "videos": ["videos.mp4","smith.mkv"], 
        "comment": "The most corrupt official ever"}

    def tearDown(self):
        response = self.test_client.get('/api/v1/red-flags',headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)))
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
        print(data)
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
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertIn(data["data"][0]["status"], "rejected")
        self.assertIn(data["data"][0]["location"], "kampala")

    def test_edit_location(self):
        response = self.test_client.post("/api/v1/red-flags",
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)), json=self.incident)
        self.assertEqual(response.status_code, 201)
        location = {"location": "mutungo"}
        res = self.test_client.patch("/api/v1/red-flags/{}/location"
        .format(response.json["data"][0]["id"]) ,
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)),json=location)
        data = json.loads(res.data)
        print(data)
        self.assertIn(data["data"][0]["message"], "Updated red-flag record's location")
        self.assertEqual(res.status_code, 200)
        
    def test_edit_comment(self):
        response = self.test_client.post("/api/v1/red-flags",
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)), json=self.incident)
        self.assertEqual(response.status_code, 201)
        comment = {"comment": "Museveni is so corrupt"}
        res = self.test_client.patch("/api/v1/red-flags/{}/comment".format(response.json["data"][0]["id"]),
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)),json=comment)
        data =json.loads(res.data)
        print(data)
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
        incident = { "createdBy": "user", "types":"redflag", "location":"Arua", 
        "status": "accepted", "images": ["image.jpg","image2"], "videos": ["videos.mp4","smith.mkv"], 
        "comment": "The most corrupt official ever"}
        response = self.test_client.post("/api/v1/red-flags",content_type='application/json',
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)), json=incident)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["Error"], "createdBy should be an integer")
       
    def test_delete_nonexistent_object(self):
        response = self.test_client.delete("/api/v1/red-flags/2",
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)))
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["status"], 404)
        self.assertIn("The red flag record with id 2 doesnt exist", data["Error"])

    def test_error_patch_invalid_id(self):
        response = self.test_client.post("/api/v1/red-flags",
         headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)), json=self.incident)
        self.assertEqual(response.status_code, 201)
        location = {"location": "mutungo"}
        response = self.test_client.patch("/api/v1/red-flags/2/location" ,
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)),json=location)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(data["status"], 404)
        self.assertIn("Non existent redflag", data["Error"])

    def test_error_patch_invalid_query_name(self):
        response = self.test_client.post("/api/v1/red-flags",
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)), json=self.incident)
        self.assertEqual(response.status_code, 201)
        response = self.test_client.patch("/api/v1/red-flags/{}/locationsa"
        .format(response.json["data"][0]["id"]),
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)))
        data = json.loads(response.data)
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

if __name__ == '__main__':
    unittest.main()