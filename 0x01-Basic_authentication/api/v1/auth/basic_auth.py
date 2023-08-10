#!/usr/bin/env python3
"""Defines BasicAuth class"""
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """Returns the decoded value of a Base64 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            de_str = base64.b64decode(base64_authorization_header)
            return de_str.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Returns user email & password from Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        val = decoded_base64_authorization_header.split(':')
        return val[0], val[1]
