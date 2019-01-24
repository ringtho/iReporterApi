import unittest
from api.views.routes import app
from tests.get_token import GetTokenTests
from api.models.redflag import RedFlag
from api.db.db_connect import Database
import json
from api.views import routes


class TestInterventions(unittest.TestCase):
    def setUp(self):
        """initialise test client"""
        self.test_client = app.test_client()
        self.db = Database()

        self.intervention = {
       
        "incident_type":"intervention", 
        "location":"0.321,35.145", 
        "status": "rejected", 
        "images": "image.jpg",
        "videos": "videos.org", 
        "comment": "my name is"
        }
        self.interventions = { "incident_type":"intervention", 
        "location":"0.321,35.145", 
        "status": "accepted", "images": "image.jpg", 
        "videos": "videos.mp4", 
        "comment": "The most corrupt official ever"}

    def tearDown(self):
        self.db.empty_tables()
        # self.db.create_users_table()
        # self.db.create_redflags_table()
        # self.db.create_interventions_table()


    def test_empty_database(self):
        response = self.test_client.get("/api/v1/red-flags", headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)))
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn(data["message"], "There are no red flags in the database")

    def test_create_interventions(self):
        getter = GetTokenTests()
        token = getter.get_user_post()
        headers={"Authorization":"Bearer " + token}
        response = self.test_client.post("/api/v1/interventions", 
        headers=headers,content_type='application/json',json=self.intervention)
        data =json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(data["data"][0]["message"], "intervention record created.")
        self.assertEqual(data["status"],201)

    def test_get_all_redflags(self):
        getter = GetTokenTests()
        token = getter.get_user_post()
        headers={"Authorization":"Bearer " + token}
        response = self.test_client.post("/api/v1/interventions",headers=headers, json=self.intervention)
        response1 = self.test_client.post("/api/v1/interventions",headers=headers, json=self.interventions)
        self.assertEqual(response.status_code, 201)
        self.assertIn(response.json["data"][0]["message"], "intervention record created.")
        self.assertIn(response1.json["data"][0]["message"], "intervention record created.")
        res = self.test_client.get("/api/v1/interventions",headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("videos.org", data["data"][0]["videos"])
        self.assertIn("videos.mp4", data["data"][1]["videos"])

    def test_get_single_intervention(self):
        getter = GetTokenTests()
        token = getter.get_user_post()
        headers={"Authorization":"Bearer " + token}
        response = self.test_client.post("/api/v1/interventions",
        headers=headers, json=self.intervention)
        self.assertEqual(response.status_code, 201)
        self.assertIn(response.json["data"][0]["message"], "intervention record created.")
        res = self.test_client.get("/api/v1/interventions/{}".format(response.json["data"][0]["id"]),
        headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn(data["data"]["videos"], "videos.org")

    def test_edit_location(self):
        getter = GetTokenTests()
        token = getter.get_user_post()
        headers={"Authorization":"Bearer " + token}
        response = self.test_client.post("/api/v1/interventions",
        headers=headers, json=self.intervention)
        self.assertEqual(response.status_code, 201)
        location = {"location":"5.056,56.234"}
        print(response.json)
        res = self.test_client.patch("/api/v1/interventions/{}/location"
        .format(response.json["data"][0]["id"]) ,
        headers=headers,json=location)
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertIn(data["data"][0]["message"], "Updated intervention record's location")
  
        
    def test_edit_comment(self):
        getter = GetTokenTests()
        token = getter.get_user_post()
        headers={"Authorization":"Bearer " + token}
        response = self.test_client.post("/api/v1/interventions",
        headers=headers, json=self.intervention)
        self.assertEqual(response.status_code, 201)
        comment = {"comment": "Museveni is so corrupt"}
        res = self.test_client.patch("/api/v1/interventions/{}/comment".format(response.json["data"][0]["id"]),
        headers=headers,json=comment)
        data =json.loads(res.data)
        # print(data)
        self.assertIn(data["data"][0]["message"], "Updated intervention record's comment")
        self.assertEqual(res.status_code, 200)
      
    def test_delete_redflag(self):
        getter = GetTokenTests()
        token = getter.get_user_post()
        headers={"Authorization":"Bearer " + token}
        response = self.test_client.post("/api/v1/interventions",
        headers=headers, json=self.intervention)
        self.assertEqual(response.status_code, 201)
        res = self.test_client.delete("/api/v1/interventions/{}".format(response.json["data"][0]["id"]),
        headers=headers)
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["data"][0]["message"], "intervention record has been deleted")
        self.assertEqual(data["status"], 200)

       
    def test_delete_nonexistent_object(self):
        response = self.test_client.delete("/api/v1/interventions/2",
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)))
        data = json.loads(response.data)
        # print(data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["status"], 404)
        self.assertIn("The intervention record with id 2 doesnt exist", data["Error"])

    def test_error_patch_invalid_id(self):
        response = self.test_client.post("/api/v1/interventions",
         headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)), json=self.intervention)
        location = {"location":"5.056,56.234"}
        response = self.test_client.patch("/api/v1/interventions/7000/location" ,
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)),json=location)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(data["status"], 404)
        self.assertIn("The intervention with id 7000 doesnt exist", data["Error"])

    def test_update_status(self):
        getter = GetTokenTests()
        token = getter.get_user_post()
        headers={"Authorization":"Bearer " + token}
        response = self.test_client.post("/api/v1/interventions",
        headers=headers, json=self.intervention)
        self.assertEqual(response.status_code, 201)
        token2 = getter.get_admin_token()
        headers={"Authorization":"Bearer " + token2}
        status = {"status":"Resolved"}
        res = self.test_client.patch("/api/v1/interventions/{}/status".format(response.json["data"][0]["id"]), headers=headers, json=status)
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["data"][0]["message"], "Updated intervention record's status to Resolved")


    def test_error_get_nonexistent_redflag(self):
        response = self.test_client.post("/api/v1/interventions",
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)), json=self.intervention)
        self.assertEqual(response.status_code, 201)
        response = self.test_client.get("/api/v1/interventions/60",
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["status"], 404)
        self.assertIn("The intervention with id 60 doesnt exist",data["Error"])

    def test_method_not_allowed(self):
        response = self.test_client.patch("/api/v1/interventions",
        headers=dict(Authorization='Bearer '+ GetTokenTests.get_user_post(self)),)
        self.assertEqual(response.status_code, 405)
        data = json.loads(response.data)
        self.assertEqual(data["Error"],"Please check to ensure to check that your" 
        " calling the right method!!")
    

   