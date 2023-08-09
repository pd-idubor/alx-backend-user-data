#!/usr/bin/env python3
"""API Authentication System"""
from flask import request
from typing import List, TypeVar


class Auth():
    """Authentication sys template"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns false"""
        if not path or not excluded_paths or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        for pat in excluded_paths:
            if pat[-1] != '/':
                path += '/'
        if path in set(excluded_paths):
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Auth header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None
