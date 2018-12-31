import unittest
from api.routes import app
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

        self.redflags = routes.redflags
        
    def test_hello_world(self):
        response = self.test_client.get("/")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(data["message"], "Hello World, it's Smith!!")
        self.assertEqual(data["status"], 200)



    # def test_empty_database(self):
    #     response = self.test_client.get("/api/v1/red-flags")
    #     self.assertEqual(response.status_code, 404)
    #     data = json.loads(response.data)
    #     self.assertIn(data["message"], "There are no red flags in the database")

    def test_create_redflag(self):
        response = self.test_client.post("/api/v1/red-flags", content_type='application/json',
        data=json.dumps(self.incident))
        data =json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(data["data"][0]["message"], "red flag record created.")
        self.assertEqual(data["data"][0]["id"], 1)
        self.assertEqual(data["status"],201)

    def test_get_all_redflags(self):
        incidents = { "id": 2,"createdOn": "Thu, 27 Dec 2018 08:04:32 GMT","createdBy": 1, "types":"redflag", "location":"kampala", 
        "status": "accepted", "images": ["image.jpg","image2"], "videos": "videos.org", 
        "comment": "my name is my name"}
        response = self.test_client.post("/api/v1/red-flags", json=incidents)
        self.assertEqual(response.status_code, 201)
        self.assertIn(response.json["data"][0]["message"], "red flag record created.")
        res = self.test_client.get("/api/v1/red-flags")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("accepted", data["data"][1]["status"])
        self.assertIn("rejected", data["data"][0]["status"])
        self.assertEqual(1, data["data"][0]["id"])
        self.assertEqual(2, data["data"][1]["id"])
        self.assertEqual(data["data"][1]["images"], ["image.jpg","image2"])
        self.assertEqual(len(data), 2)

    def test_get_single_redflag(self):
        res = self.test_client.get("/api/v1/red-flags/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["data"][0]["id"], 1)
        self.assertIn(data["data"][0]["status"], "rejected")
        self.assertEqual(len(data), 2)
        self.assertIn(data["data"][0]["location"], "mutungo")

    def test_edit_location(self):
        location = {"location": "mutungo"}
        res = self.test_client.patch("/api/v1/red-flags/1/location" ,json=location)
        data = json.loads(res.data)
        self.assertIn(data["data"][0]["message"], "Updated red-flag record's location")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["data"][0]["id"], 1)

    def test_edit_comment(self):
        comment = {"comment": "Museveni is so corrupt"}
        res = self.test_client.patch("/api/v1/red-flags/1/comment" ,json=comment)
        data =json.loads(res.data)
        self.assertIn(data["data"][0]["message"], "Updated red-flag record's comment")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["data"][0]["id"], 1)

    # def test_delete_redflag(self):
    #     incidents = { "id": 2,"createdOn": "Thu, 27 Dec 2018 08:04:32 GMT","createdBy": 1, "types":"redflag", "location":"kampala", 
    #     "status": "accepted", "images": ["image.jpg","image2"], "videos": "videos.org", 
    #     "comment": "my name is my name"}
    #     response = self.test_client.post("/api/v1/red-flags" ,json=incidents)
    #     self.assertEqual(response.status_code, 201)
    #     res = self.test_client.delete("/api/v1/red-flags/2")
    #     data = json.loads(res.data)
    #     print(data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["data"][0]["message"], "red-flag record has been deleted")
    #     self.assertEqual(data["data"][0]["id"],1)
    #     self.assertEqual(data["status"], 200)

    def test_createdBy_string(self):
        incidents = { "id": 2,"createdOn": "Thu, 27 Dec 2018 08:04:32 GMT","createdBy": '1', "types":"redflag", "location":"kampala", 
        "status": "accepted", "images": ["image.jpg","image2"], "videos": "videos.org", 
        "comment": "my name is my name"}
        response = self.test_client.post("/api/v1/red-flags",content_type='application/json', data=json.dumps(incidents))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["Error"], "CreatedBy should be an int")
        self.assertEqual(response.json["status"], 400)

    def test_delete_nonexistent_object(self):
        response = self.test_client.delete("/api/v1/red-flags/4")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["status"], 404)
        self.assertIn("The red flag record with id 4 doesnt exist", data["Error"])

    def test_error_patch_invalid_id(self):
        response = self.test_client.patch("/api/v1/red-flags/4/location")
        data = json.loads(response.data)
        self.assertEqual(data["status"], 404)
        self.assertIn("Non existent redflag", data["Error"])

    def test_error_patch_invalid_query_name(self):
        response = self.test_client.patch("/api/v1/red-flags/1/locationsa")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["status"], 404)
        self.assertIn("The url you provided doesnt exist", data["message"])

    def test_error_get_nonexistent_redflag(self):
        response = self.test_client.get("/api/v1/red-flags/4")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["status"], 404)
        self.assertIn("A redflag with an id of 4 doesnt exist",data["Error"])

    def test_error_page_not_found(self):
        response = self.test_client.post("/abc")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["Issue"], "You have entered an unknown URL.")

    def test_method_not_allowed(self):
        response = self.test_client.patch("/api/v1/red-flags")
        self.assertEqual(response.status_code, 405)
        data = json.loads(response.data)
        self.assertEqual(data["Error"],"Please check to ensure to check that your" 
        " calling the right method!!")

if __name__ == '__main__':
    unittest.main()