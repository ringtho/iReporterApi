import jwt

secret_key = "my_name_is_my_name"

def encode_token(user_id, username):
    payload = {
        "uid": user_id,
        "unm": username,
       
    }

    token = jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')
    return token

