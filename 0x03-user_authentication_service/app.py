#!/usr/bin/env python3
"""
Flask app
"""

from flask import Flask, jsonify, request, abort, make_response
from flask import redirect, url_for
from auth import Auth


app = Flask(__name__)

AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome():
    """
    GET route that returns a JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """
    POST /users route to register a new user
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"message": "email is required"}), 400
    if not password:
        return jsonify({"message": "password is required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    except Exception as e:
        return jsonify({"message": "unexpected error occurred"}), 500


@app.route("/sessions", methods=["POST"])
def login():
    """
    POST /sessions route to log in a user and create a session
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        abort(401)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)

    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """
    DELETE /sessions route to log out a user
    """
    session_id = request.cookies.get("session_id")

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect(url_for("welcome"))


@app.route("/profile", methods=["GET"])
def profile():
    """
    GET /profile route to get user profile
    """
    session_id = request.cookies.get("session_id")

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """
    PUT /reset_password route to update a user's password.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    if not email or not reset_token or not new_password:
        return jsonify(
            {
                "message": "email, reset_token, and new_password are required"
                }), 400

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        return abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
