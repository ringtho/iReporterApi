from flask import Flask, jsonify, request, json
from api.models import RedFlag
from api.user import (User, users, get_user)
from api.validator import Validator
from api.resources.auth import encode_token
from api.resources.auth import required_token
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

redflags = []


@app.route("/")
def hello():
    return jsonify({"status": 200,"message":"Hello World, it's Smith!!"}),200

@app.route("/api/v1/red-flags" ,methods=["POST"])
@required_token
def create_redflag():
    validator = Validator(request)
    if validator.redflag_is_valid():
        data = request.get_json()
        redflag = RedFlag(createdBy = data["createdBy"], types = data["types"], 
        location = data["location"],status = data["status"], images = data["images"], 
        videos = data["videos"],comment = data["comment"])
        redflags.append(redflag.json_format())
        return jsonify({"status": 201, "data": [{ "id": redflags[-1]["id"],
        "message": "red flag record created."}]}), 201
    else:
        return jsonify({"status": 400, "Error": validator.error}), 400
 
@app.route("/api/v1/red-flags", methods=["GET"])
@required_token
def get_redflags():
    if len(redflags) < 1:
        return jsonify({"status": 404, "message":"There are no red flags in the database"}), 404
    return jsonify({"status": 200, "data": redflags }), 200

@app.route("/api/v1/red-flags/<int:red_flag_id>", methods=["GET"])
@required_token
def get_single_redflag(red_flag_id):
    single_redflag = []
    if len(redflags) < 1:
        return jsonify({"status": 404, "Error": "There are no redflags present in the database"}),404
    for redflag in redflags:
        if redflag["id"] == red_flag_id:
            single_redflag.append(redflag)
            return jsonify({"status": 200, "data": single_redflag}), 200
    return jsonify({"status": 404, "Error": "A redflag with an id of {} doesnt exist".format(red_flag_id)}),404   
       
@app.route("/api/v1/red-flags/<int:red_flag_id>/<string:query>", methods=['PATCH'])
@required_token
def edit_location(red_flag_id, query):
    validator = Validator(request)
    if validator.valid_location_for_edit():
        for redflag in redflags:
            if redflag["id"] == red_flag_id:
                data = request.get_json()
                if (query == "location") or (query == "comment"):
                    redflag[query] = data[query]
                    return jsonify({"status":200, "data": [{"id": red_flag_id,
                    "message": "Updated red-flag record's " + query }]})
                return jsonify({"status": 404, "message": "The url you provided doesnt exist"
                ", Try http://127.0.0.1:5000/api/v1/red-flags/1/query where query can be 'comment'"
                " or 'location'"}),404
        return jsonify({"status": 404, "Error": f"Non existent redflag. Id {red_flag_id} doesnt exist!"}),404
    return jsonify({"status": 400, "Error": validator.error}), 400

@app.route("/api/v1/red-flags/<int:red_flag_id>" ,methods=['DELETE'])
@required_token
def delete_redflag(red_flag_id):
    for redflag in redflags:
        if redflag['id'] == red_flag_id:
            redflags.remove(redflag)
            return jsonify({
            "status": 200,
            "data":[{"id": redflag['id'],"message":"red-flag record has been deleted"}]
            })
    return jsonify({"status": 404, "Error": f"The red flag record with id {red_flag_id} doesnt exist"}),404

@app.route("/api/v1/auth/register", methods=["POST"])
def create_user():
    validator = Validator(request)
    data = request.get_json()
    if validator.validate_user_data():
        user = User(firstname = data['firstname'], lastname = data['lastname'],
        othernames = data['othernames'], email = data['email'], phoneNumber = data['phoneNumber'],
        username = data['username'], password = generate_password_hash(data['password']))
        new_user = user.json_format()
        users.append(new_user)
        return jsonify({"status": 201, "data":[{"user": {
            "id": users[-1]["id"],
            "username": users[-1]["username"]
        },
           "message":"User successfully created"}]}),201
    return jsonify({"status": 400, "Error": validator.error})

@app.route("/api/v1/auth/login", methods=["POST"])
def login_user():
    data = request.get_json()
    if not data:
    
        return jsonify({"Error": "Please provide some data!"})
    
    username = data["username"]
    password = data["password"]

 
    response = get_user(username, password)
    print(response)
   
   
    if response:
        _id = response["id"]
        isAdmin = response["isAdmin"]
        token = encode_token(_id,username, isAdmin)
        return jsonify({
            "status": 201, "data": [{
            "username": response["username"],
            "message": "Logged in successfully",
            "token": token
            }]
        }), 201
    return jsonify({ "status": 400, "Error": "Invalid Username or Password"}), 400 

     

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

