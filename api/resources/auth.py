import jwt
from flask import request, jsonify
import datetime
from functools import wraps

secret_key = "my_name_is_my_name"

def encode_token(user_id, username, isAdmin=False):
    payload = {
        "uid": user_id,
        "unm": username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=1),
        'adm': isAdmin
       
    }

    token = jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')
    return token

def ensure_token_available_and_clean():
    header_token = request.headers.get("Authorization")
    if not header_token:
        return jsonify({"status": 400, "Error":"Missing token!!"}),400
    elif "Bearer" not in header_token:
        return jsonify({"status": 400, "Error": "Token tampered with!!!"}),400
    token = header_token.split(" ")[1]
    return token 

def decode_token(token):
    """
        Decode the token back to original state before sending
    """
    decode = jwt.decode(token, secret_key, algorithms='HS256')
    return decode

def get_id_token():
    token = ensure_token_available_and_clean()
    decoded = decode_token(token)
    user_id = decoded["uid"]
    return user_id

def required_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = None
        try:
            token = ensure_token_available_and_clean()
            token = decode_token(token)
            response = func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            response = jsonify({
                "status": 401,
                "Error": "Token has expired!!"
            }),401
        except jwt.InvalidTokenError:
            response = jsonify({
                "status": 401,
                "Error": "Invalid token. Please provide a valid token"
            }),401
        return response
    return wrapper

def admin_or_user():
    """
        check if a user is an admin or not
    """
    user = decode_token(ensure_token_available_and_clean())
    user_type = user["adm"]
    return user_type

def check_user_id():
    user = decode_token(ensure_token_available_and_clean())
    user_id = user["uid"]
    return user_id

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not admin_or_user():
            response = {
                "status": 403,
                "Error": "Admin priviledges required to access this resource!"
            }
            return response, 403
        return func(*args, **kwargs)
    return wrapper



