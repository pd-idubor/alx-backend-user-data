#!/usr/bin/env python3
"""Basic Flask app"""
from flask import Flask, jsonify
from auth import Auth
import requests


AUTH = Auth()
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index() -> str:
    """Index page"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', method=['POST'], strict_slashes=False)
def users() -> str:
    """Register user"""
    email = requests.request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
