#!/usr/bin/env python3
"""Defines SessionAuth class"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """For auth. mechanism"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates Session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        else:
            session_id = str(uuid.uuid4())
            SessionAuth.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value"""
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        return User.get(user_id)
