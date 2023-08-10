#!/usr/bin/env python3
"""SessionExpAuth"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """SessionExpAuth"""
    def __init__(self):
        """Initialization"""
        super().__init__()
        session_duration = os.getenv('SESSION_DURATION')
        try:
            self.session_duration = int(session_duration)
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create session id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """User_id for session_id"""
        if session_id is None:
            return None
        if self.user_id_by_session_id.get(session_id) is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        
        created_at = session_dict.get("created_at")
        if created_at is None:
            return None
        calc_time = created_at + timedelta(seconds=self.session_duration)
        if calc_time < datetime.now():
            return None
        return session_dict.get("user_id")
