from flask import Flask, jsonify, request
from api.models import RedFlag


app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify({"message":"Hello World, it's Smith!!"}),200