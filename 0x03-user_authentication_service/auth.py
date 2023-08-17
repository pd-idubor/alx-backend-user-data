#!/usr/bin/env python3
"""Hash password"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Save the user to the database using self._db
        and return the User object"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            hashed = _hash_password(password)
            return self._db.add_user(email, hashed)

    def valid_login(self, email: str, password: str) -> bool:
        """Credentials validation"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except (NoResultFound):
            return False

    def create_session(self, email) -> str:
        """Returns the session ID as a string"""
        try:
            user = self._db.find_user_by(email=email)
            uuid = _generate_uuid()
            self._db.update_user(user.id, session_id=uuid)
            return uuid
        except NoResultFound:
            return

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Find user by session ID"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy session with user ID"""
        if user_id is None:
            return None
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate a UUID and update the user’s
        reset_token database field"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed = _hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=hashed,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
        return None

def _hash_password(password: str) -> bytes:
    """Returns salted hash of the input password"""
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """UUID gen"""
    return str(uuid.uuid4())
