#!/usr/bin/env python3
"""
Route module for the API.
"""

from os import getenv
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from api.v1.views import app_views

# Initialize Flask app
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize auth
auth = None
auth_type = getenv("AUTH_TYPE")

if auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth

    auth = BasicAuth()
elif auth_type == "auth":
    from api.v1.auth.auth import Auth

    auth = Auth()


# before_request handler
@app.before_request
def before_request():
    """
    Validates requests before processing.

    - If auth is None, do nothing.
    - Checks if the request path is part of the excluded paths.
    - Verifies the authorization header and the current user.
    """
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']

    if auth:
        if not auth.require_auth(request.path, excluded_paths):
            return  # No authentication needed for this path

        # Check if Authorization header is present
        if auth.authorization_header(request) is None:
            abort(401)

        # Check if current user is valid
        if auth.current_user(request) is None:
            abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handles 404 Not Found errors by returning a JSON response.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Handles 401 Unauthorized errors by returning a JSON response.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Handles 403 Forbidden errors by returning a JSON response.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    try:
        port = int(port)
    except ValueError:
        port = 5000
    app.run(host=host, port=port)
