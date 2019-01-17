import jwt
from api.routes import app

secret_key = "my_name_is_my_name"
app.config['JWT_SECRET_KEY'] = 'secret-key'

def encode_token(user_id, isAdmin):
    payload = {
        "uid": user_id,
        "adm": isAdmin,
        "exp": ""
    }

    token = jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')
    return token