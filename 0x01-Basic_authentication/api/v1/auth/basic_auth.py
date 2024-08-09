#!/usr/bin/env python3
""" BasicAuth module
"""

from api.v1.auth.auth import Auth
from models.user import User
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
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes Base64 part of the Authorization header
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user cedentials from decoded Base64 Auth header
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> User:
        """
        Retrieves User instance based on email & password
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        try:
            user_list = User.search({'email': user_email})
            if not user_list:
                return None

            for user in user_list:
                if user.is_valid_password(user_pwd):
                    return user

        except Exception:
            return None

        return None
