#!/usr/bin/env python3
"""
Flask app module
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from typing import Tuple, Union


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def welcome() -> Tuple[str, int]:
    """Welcome route
    Returns:
        str: JSON response
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'])
def users() -> Tuple[str, int]:
    """Register new user route
    Returns:
        str: JSON response
        int: Status code
    """
    try:
        email = request.form['email']
        password = request.form['password']
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> Tuple[str, int]:
    """Login user route
    Returns:
        str: JSON response
        int: Status code
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """Logout user route
    Returns:
        str: Redirect to home page
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'])
def profile() -> Union[str, Tuple[str, int]]:
    """Get user profile route
    Returns:
        str: JSON response
        int: Status code
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> Union[str, Tuple[str, int]]:
    """Get reset password token route
    Returns:
        str: JSON response
        int: Status code
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({
            "email": email,
            "reset_token": reset_token
        }), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> Union[str, Tuple[str, int]]:
    """Update password route
    Returns:
        str: JSON response
        int: Status code
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({
            "email": email,
            "message": "Password updated"
        }), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
