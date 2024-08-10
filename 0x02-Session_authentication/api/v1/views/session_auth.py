#!/usr/bin/env python3
"""
Session Authentication View
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Handle login for session authentication
    """
    from api.v1.app import auth

    # Get email and password from the form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email is missing
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    # Check if password is missing
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    # Retrieve the User instance based on the email
    try:
        users = User.search({"email": email})
    except Exception:
        users = None

    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # Check if the password is correct
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a Session ID for the User ID
    session_id = auth.create_session(user.id)

    # Create a response with the user details
    response = jsonify(user.to_json())

    # Set the session ID in the cookie
    session_name = getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)

    return response
