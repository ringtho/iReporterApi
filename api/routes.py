from flask import Flask, jsonify, request
from api.models import RedFlag


app = Flask(__name__)

redflags = []
count = 0

@app.route("/")
def hello():
    return jsonify({"message":"Hello World, it's Smith!!"}),200

@app.route("/api/v1/red-flags" ,methods=["POST"])
def create_redflag():
    data = request.get_json()
    global count
    try:
        print(data)
        if type(data["createdBy"]) is not int:
            raise ValueError("createdBy field only takes an integer")
        count+=1
        redflag = RedFlag(count,createdBy = data["createdBy"], types = data["types"], 
        location = data["location"],status = data["status"], images = data["images"], 
        videos = data["videos"],comment = data["comment"])
        redflags.append(redflag.json_format())
    except ValueError as e:
        print(e)
        return jsonify({"status": 400, "Error": "CreatedBy should be an int"}), 400
    return jsonify({"status": 201, "data": [{ "id": redflags[-1]["id"],
    "message": "red flag record created."}]}), 201