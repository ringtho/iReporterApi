from flask import Flask, jsonify, request
from api.models import RedFlag


app = Flask(__name__)

redflags = []

@app.route("/")
def hello():
    return jsonify({"message":"Hello World, it's Smith!!"}),200

@app.route("/api/v1/red-flags" ,methods=["POST"])
def create_redflag():
    data = request.get_json()
    try:
        print(data)
        if type(data["createdBy"]) is not int:
            raise ValueError("createdBy field only takes an integer")
        redflag = RedFlag(createdBy = data["createdBy"], types = data["types"], location = data["location"],
        status = data["status"], images = data["images"], videos = data["videos"], 
        id = data["id"],comment = data["comment"])
        redflags.append(redflag.json_format())
    except ValueError as e:
        print(e)
        return jsonify({"status": 400, "Error": "CreatedBy should be an int"}), 400
    return jsonify({"status": 201, "data": [{ "id": redflags[0]["id"],
    "message": "red flag record created."}]}), 201

@app.route("/api/v1/red-flags", methods=["GET"])
def get_redflags():
    redflag_entry = []
    print(redflags)

    for redflag in redflags:
        redflag_entry.append(redflag)

    print(redflag_entry)
    if len(redflag_entry) < 1:
        return jsonify({"status": 200, "message":"There are no red flags created"}), 200
    return jsonify({"status": 200, "data": redflag_entry }), 200

@app.route("/api/v1/red-flags/<int:red_flag_id>", methods=["GET"])
def get_single_redflag(red_flag_id):
    single_redflag = []
    for redflag in redflags:
        if redflag["id"] == red_flag_id:
            single_redflag.append(redflag)
        print(single_redflag)

        if len(single_redflag) < 1:
            return jsonify({"status": 200, "Error": "There are no redflags in the database"})

        return jsonify({"status": 200, "data": single_redflag}), 200

@app.route("/api/v1/red-flags/<int:red_flag_id>/<string:query>", methods=['PATCH'])
def edit_location(red_flag_id, query):
    for redflag in redflags:
        if redflag["id"] == red_flag_id:
            data = request.get_json()
            if (query == "location"):
                redflag[query] = data[query]
                print(redflag[query])
                return jsonify({"status":200, "data": [{"id": red_flag_id,
                "message": "Updated red-flag record's " + query }]})
            return jsonify({"status": 200, "message": "The url you provided doesnt exist"
             ", Try http://127.0.0.1:5000/api/v1/red-flags/{id}/location"})