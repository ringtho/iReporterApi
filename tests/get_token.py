from api.views.routes import create_app
from flask import json

app = create_app("testing")

class GetTokenTests:
    

    def get_user_post(self):
        register_info = {
        
            "firstname": "smith",
            "lastname": "Ringtho",
            "othernames": "J",
            "email": "sringtho@gmail.com",
            "phoneNumber": "+256778339655",
            "username": "sringtho1",
            "password": "Sr654321"

        }
    
        response = create_app("testing").test_client().post('/api/v1/auth/signup', json=register_info)

        admin={
            
            "firstname": "smith",
            "lastname": "ringtho",
            "othernames": "J",
            "email": "admin@gmail.com",
            "phoneNumber": "+256778339655",
            "username": "admin",
            "password": "Sr654321"

        }

        response = app.test_client().post('/api/v1/auth/admin', json=admin)

        user = {

                "username": "admin",
                "password": "Sr654321"

            }

        response = app.test_client().post('/api/v1/auth/login', json=user)
        token = json.loads(response.data)["data"][0]['token']
        # print(token)
        return token
        
     
        
        

    def get_admin_token(self):
        admin={
            
            "firstname": "smith",
            "lastname": "ringtho",
            "othernames": "J",
            "email": "admin@gmail.com",
            "phoneNumber": "+256778339655",
            "username": "admin",
            "password": "Sr654321"

        }

        response = app.test_client().post('/api/v1/auth/admin', json=admin)
        
        admin = {

                "username": "admin",
                "password": "Sr654321"

            }

        response = app.test_client().post('/api/v1/auth/login', json=admin)
        token = json.loads(response.data)["data"][0]['token']
        print(token)
        return token


    