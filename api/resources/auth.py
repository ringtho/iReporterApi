import jwt
from flask import request, jsonify
import datetime
from functools import wraps

secret_key = "my_name_is_my_name"

def encode_token(user_id, username):
    payload = {
        "uid": user_id,
        "unm": username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=60),
       
    }

    token = jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')
    return token

def ensure_token_available_and_clean():
    header_token = request.headers.get("Authorization")
    if not header_token:
        return jsonify({"status": 400, "Error":"Missing token!!"})
    elif "Bearer" not in header_token:
        return jsonify({"status": 400, "Error": "Token tampered with!!!"})
    token = header_token.split(" ")[1]
    return token 

def decode_token(token):
    """
        Decode the token back to original state before sending
    """
    decode = jwt.decode(token, secret_key, algorithms='HS256')
    return decode

def required_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = None
        try:
            token = ensure_token_available_and_clean()
            decode_token(token)
            response = func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            response = jsonify({
                "status": 401,
                "error": "Token has expired!!"
            })
        except jwt.InvalidTokenError:
            response = jsonify({
                "status": 401,
                "Error": "Invalid token"
            })
        return response
    return wrapper

