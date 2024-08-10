# api/v1/views/session_auth.py
""" Session Authentication Views
"""
from flask import request, jsonify, make_response
from models.user import User
from api.v1.app import auth  # Import auth here to avoid circular imports

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ Handles POST requests for login """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    response = make_response(user.to_json())
    response.set_cookie(getenv('SESSION_NAME'), session_id)

    return response
