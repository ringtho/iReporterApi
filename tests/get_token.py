from api.routes import app
from flask import json

class GetTokenTests:

    def get_user_post(self):
        register_info = {
        
            "firstname": "smith",
            "lastname": "Ringtho",
            "othernames": "J",
            "email": "sringtho@gmail.com",
            "phoneNumber": "0778339655",
            "username": "sringtho1",
            "password": "sr654321"

        }
    
        response = app.test_client().post('/api/v1/auth/register', json=register_info)
        user = {

                "username": "sringtho1",
                "password": "sr654321"

            }

        response = app.test_client().post('/api/v1/auth/login', json=user)
        token = json.loads(response.data)["data"][0]['token']
        return token


    