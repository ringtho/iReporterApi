# from flask import Flask, jsonify, request, json
# from api.models.interventions import Intervention
# from api.views.routes import app
# from api.validator import Validator
# from api.resources.auth import get_id_token
# from api.resources.auth import required_token
# from api.db.db_connect import Database

# intervention_obj = Intervention()

# @app.route("/api/v1/interventions" ,methods=["POST"])
# @required_token
# def create_intervention():
#     validator = Validator(request)
#     user_id = get_id_token()
#     cursor = Database().cursor
#     if validator.redflag_is_valid():
#         data = request.get_json()
#         intervention_obj.create_intervention(data["incident_type"], data["location"],user_id,data["images"], 
#         data["videos"],data["comment"], "DRAFT")
#         query = "SELECT id FROM redflags ORDER BY id DESC"
#         cursor.execute(query)
#         redflag_id = cursor.fetchone()["id"]
#         return jsonify({"status": 201, "data": [{ "id":redflag_id,
#         "message": "red flag record created."}]}), 201
#     else:
#         return jsonify({"status": 400, "Error": validator.error}), 400