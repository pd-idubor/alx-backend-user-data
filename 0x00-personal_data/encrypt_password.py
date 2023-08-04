#!/usr/bin/env python3
"""Perform hashing using bcrypt package"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashing"""
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed
