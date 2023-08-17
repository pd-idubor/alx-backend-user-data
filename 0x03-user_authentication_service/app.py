#!/usr/bin/env python3
"""Basic Flask app"""
from flask import Flask, jsonify, request, abort, redirect
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index() -> str:
    """Index page"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """Register user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Log in"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password) is False:
        abort(401)
    else:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """Log out"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
