#!/usr/bin/env python3
""" BasicAuth module
"""

from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """ BasicAuth class that inherits from Auth """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts Base64 part of Authorization header for Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        
        try:
            decoded_bytes = base64.b64decode(authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None
