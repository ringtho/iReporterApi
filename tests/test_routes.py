import unittest
from api.routes import app
import json

class TestRedFlags(unittest.TestCase):
    def setUp(self):
        """initialise test client"""
        self.test_client = app.test_client()
        self.incident = {
        "id": 1, 
        "createdBy": 1, 
        "types":"redflag", 
        "location":"kampala", 
        "status": "rejected", 
        "images": "image.jpg", 
        "videos": "videos.org", 
        "comment": "my name is"
        }

    def test_create_redflag(self):
        response = self.test_client.post("/api/v1/red-flags", json=self.incident)
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

    def test_delete_redflag(self):
        res = self.test_client.delete("/api/v1/red-flags/2")
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["Error"], "The red flag record doesnt exist or already deleted")
        self.assertEqual(data["status"], 200)
        

    

if __name__ == '__main__':
    unittest.main()