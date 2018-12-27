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


if __name__ == '__main__':
    unittest.main()