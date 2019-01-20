import jwt
from flask import jsonify, request
from functools import wraps
from api.resources.auth import secret_key
from api.resources.auth import decode_token


def ensure_token_valid():
    token = request.headers.get('Authorization')
    if not token:
        raise Exception('Token not specified.')
    if token.strip()[:7] != 'Bearer ':
        raise Exception('Invalid token prefix.')
    return token.split()[1]


def is_admin():
    token = ensure_token_valid()
    payload = decode_token(token)
    # payload = jwt.decode(token.encode(), algorithm='HS256', verify=False)
    return payload['adm']


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if is_admin():
                return func(*args, **kwargs)
            return jsonify({"status":403, 'Error': 'Admin privileges required.'}), 403
        except Exception as e:
            if isinstance(e, jwt.InvalidTokenError):
                return jsonify({"status":401, 'Error': 'Token could not be decoded.'}), 401
            return jsonify({"status":401, 'Error': str(e)}), 401
    return wrapper