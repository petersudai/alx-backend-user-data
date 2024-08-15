#!/usr/bin/env python3
"""
Basic Flask app
"""

from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)


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
    password = request.form.gete("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
