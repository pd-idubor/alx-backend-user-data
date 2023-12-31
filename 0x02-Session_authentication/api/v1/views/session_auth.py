#!/usr/bin/env python3
"""New view for Session Authentication"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login() -> str:
    """Route"""
    email = request.form.get('email')
    pwd = request.form.get('password')
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if pwd is None or pwd == "":
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    if user is None or len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if not user.is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    cookie = os.getenv("SESSION_NAME")
    response = jsonify(user.to_json())
    response.set_cookie(cookie, session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def auth_session_logout() -> str:
    """Deletes the Session ID in request as cookie"""
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
