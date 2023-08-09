#!/usr/bin/env python3
"""API Authentication System"""
from flask import request
from typing import List, TypeVar


class Auth():
    """Authentication sys template"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns false"""
        return False

    def authorization_header(self, request=None) -> str:
        """Auth header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None
