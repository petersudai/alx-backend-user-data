#!/usr/bin/env python3
""" BasicAuth module
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class that inherits from Auth """

    def extract_based64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts Base64 part of Authorization header for Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]
