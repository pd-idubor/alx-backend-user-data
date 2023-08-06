#!/usr/bin/env python3
"""Perform hashing using bcrypt package"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashing"""
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Pasword hashing validation"""
    if bcrypt.checkpw(password.encode(), hashed_password):
        return True
    else:
        return False
