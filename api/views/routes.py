from flask import Flask, jsonify, request, json
from api.models.redflag import RedFlag
from api.models.user import (User, users)
from api.validator import Validator
from api.resources.auth import encode_token
from api.resources.auth import decode_token
from api.resources.auth import get_id_token
from api.models.user import User
from api.resources.auth import required_token
from api.resources.admin_auth import admin_required
from api.db.db_connect import Database
from werkzeug.security import generate_password_hash, check_password_hash





app = Flask(__name__)

# db_obj.create_tables


redflags = []
redflag_obj = RedFlag()
validator = Validator(request)
cursor = Database().cursor

@app.route("/")
def hello():
    return jsonify({"status": 200,"message":"Hello World, it's Smith!!"}),200

@app.route("/api/v1/red-flags" ,methods=["POST"])
@required_token
def create_redflag():
    validator = Validator(request)
    user_id = get_id_token()
    if validator.redflag_is_valid():
        data = request.get_json()
        redflag_obj.create_redflag(data["incident_type"], data["location"],user_id,data["images"], 
        data["videos"],data["comment"], "DRAFT")
        query = "SELECT id FROM redflags ORDER BY id DESC"
        cursor.execute(query)
        redflag_id = cursor.fetchone()["id"]
        return jsonify({"status": 201, "data": [{ "id":redflag_id,
        "message": "red flag record created."}]}), 201
    else:
        return jsonify({"status": 400, "Error": validator.error}), 400
 
@app.route("/api/v1/red-flags", methods=["GET"])
@required_token
def get_redflags():
    user_id = get_id_token()
    redflags = redflag_obj.get_redflag_records(user_id)
    if redflags:
        return jsonify({"status": 200, "data": redflags }), 200
    return jsonify({"status": 404, "message":"There are no red flags in the database"}), 404
    

@app.route("/api/v1/red-flags/<int:red_flag_id>", methods=["GET"])
@required_token
def get_single_redflag(red_flag_id):
    user_id = get_id_token()
    record = redflag_obj.get_single_redflag(red_flag_id, user_id)
    print(record)
    if record:
        return jsonify({"status": 200, "data": record}), 200
    return jsonify({"status": 404, "Error": f"The redflag with id {red_flag_id} doesnt exist"}),404
  
       
@app.route("/api/v1/red-flags/<int:red_flag_id>/location", methods=['PATCH'])
@required_token
def edit_location(red_flag_id):
    if validator.valid_location_for_edit():
        user_id = get_id_token()
        data = request.get_json()
        location = data["location"]
        record = redflag_obj.edit_location(red_flag_id,location,user_id)
        if record:
            return jsonify({"status":200, "data": [{"id": red_flag_id,
            "message": "Updated red-flag record's location" }]})
        return jsonify({"status": 404, "Error": f"The redflag with id {red_flag_id} doesnt exist"}),404
    return jsonify({"status": 400, "Error":validator.error})    

@app.route("/api/v1/red-flags/<int:red_flag_id>/comment", methods=['PATCH'])
@required_token
def edit_comment(red_flag_id):
    user_id = get_id_token()
    data = request.get_json()
    comment = data["comment"]
    record = redflag_obj.edit_comment(red_flag_id,comment,user_id)
    if record:
        return jsonify({"status":200, "data": [{"id": red_flag_id,
        "message": "Updated red-flag record's comment" }]})
    return jsonify({"status": 404, "Error": f"The redflag with id {red_flag_id} doesn't exist"}),404


@app.route("/api/v1/red-flags/<int:red_flag_id>" ,methods=['DELETE'])
@required_token
def delete_redflag(red_flag_id):
    user_id = get_id_token()
    delete = redflag_obj.delete_redflag_record(red_flag_id,user_id)
    if delete:
        return jsonify({
            "status": 200,
            "data":[{"id": red_flag_id,"message":"red-flag record has been deleted"}]
            })
    return jsonify({"status": 404, "Error": f"The red flag record with id {red_flag_id} doesnt exist"}),404

@app.route("/api/v1/auth/signup", methods=["POST"])
def create_user():
    data = request.get_json()
    validator = Validator(request)
    if validator.validate_user_data():
        user_obj = User()
        password = generate_password_hash(data['password'])
        user_obj.create_user(data['firstname'], data['lastname'], data['othernames'], 
        data['username'], data['phoneNumber'], password, data['email'],False)
        del data["password"]
        return jsonify({"status": 201, "data":[{"user": {
            "token": "token",
            "user": data
        },
        "message":"User successfully created"}]}),201
    return jsonify({"status": 400, "Error": validator.error}),400
    

@app.route("/api/v1/auth/login", methods=["POST"])
def login_user():
    data = request.get_json()
    user = User()
    if not data:
        return jsonify({"Error": "Please provide some data!"}), 400
    if validator.validate_login_data():
        username = data["username"]
        password = data["password"]
        response = user.get_user(username, password)
        print(response)
        if response:
            _id = response["id"]
            isAdmin = response["isadmin"]
            token = encode_token(_id,username, isAdmin)
            return jsonify({
                "status": 200, "data": [{
                "token": token,
                "user": response
                }]
            }), 200
        return jsonify({ "status": 400, "Error": "Invalid Username or Password"}), 400 
    return jsonify({"status": 400, "Error": validator.error})

@app.route("/api/v1/auth/users",methods=["GET"])
@admin_required
def get_user_info():
    if len(users) < 1:
        return jsonify({"status": 404, "Error": "There are no users in the database"}),404
    return jsonify({"status": 200,"data": users}), 200

@app.route("/api/v1/auth/users/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_user(user_id):
    for user in users:
        if user['id'] == user_id:
            users.remove(user)
            return jsonify({
            "status": 200,
            "data":[{"id": user['id'],"message":"{} has been deleted from the system".format(user["username"])}]
            })
    return jsonify({"status": 404, "Error": f"The user with id {user_id} doesnt exist"}),404  


     

@app.errorhandler(404)
def page_doesnt_exist(e):
    valid_urls = {
        'POST a redflag': {'url': '/api/v1/red-flags', 'method(s)': 'POST', 'body': {'id':'int', 'createdBy':'int','createdOn':'datetime',
        'type':'string','location':'string','status':'string','images':'image', 'videos':'videos','comment':'string'
         }},
        'GET all redflags': {'url': '/api/v1/red-flags', 'method(s)': 'GET'},
        'GET single redflag': {'url': '/api/v1/red-flags/red_flag_id', 'method(s)': 'GET'},
        'DELETE a redflag': {'url': '/api/v1/red-flags/red_flag_id', 'method(s)': 'DELETE'},
        'EDIT location of a redflag': {'url': '/api/v1/red-flags/red_flag_id/location', 'method(s)': 'PATCH'},
        'EDIT comment of a redflag': {'url': '/api/v1/red-flags/red_flag_id/comment', 'method(s)': 'PATCH'},
        'GET HelloWorld': {'url': '/', 'method(s)': 'GET'}
    }
    return jsonify ({
        'Issue': 'You have entered an unknown URL.',
        'Valid URLs': valid_urls,
        'message': 'Please contact Smith Ringtho for more details on this API.'
        }), 404
        
@app.errorhandler(405)
def method_not_allowed(self):
    methods = [{"PATCH": "editing a redflag", "GET":"retrieving redflags", 
    "POST":"creating a redflag","DELETE":"deleting a redflag"}]

    return jsonify({
        "status": 405, 
        "Error": "Please check to ensure to check that your calling the right method!!",
        "Methods": methods
    }), 405

