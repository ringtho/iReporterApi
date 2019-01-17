import jwt
from flask import request, jsonify

secret_key = "my_name_is_my_name"

def encode_token(user_id, username):
    payload = {
        "uid": user_id,
        "unm": username,
       
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