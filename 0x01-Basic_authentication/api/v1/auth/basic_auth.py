#!/usr/bin/env python3
"""Defines BasicAuth class"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header.startswith("Basic ") is False:
            return None
        else:
            return authorization_header[6:]
