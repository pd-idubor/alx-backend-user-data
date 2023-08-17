#!/usr/bin/env python3
"""Hash password"""
import bcrypt
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Save the user to the database using self._db
        and return the User object"""
        user = self._db._session.query(User).filter_by(email=email).first()
        if user:
            raise ValueError('User {} already exists'.format(email))
        else:
            hashed = _hash_password(password)
            self._db.add_user(email, password)


def _hash_password(password: str) -> bytes:
    """Returns salted hash of the input password"""
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed
