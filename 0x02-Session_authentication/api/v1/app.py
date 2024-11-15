#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from api.v1.views import app_views
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize BasicAuth
auth = BasicAuth()

@app.before_request
def before_request():
    """ Function to assign the current user before each request """
    request.current_user = auth.current_user(request)

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler """
    return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
