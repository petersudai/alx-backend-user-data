#!/usr/bin/env python3
""" BasicAuth module
"""

from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64

UserType = TypeVar('User', bound=User)


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

    def current_user(self, request=None) -> UserType:
        """
        Overload Auth's current_user to retrieve User instance for request
        """
        if request is None:
            return None

        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None

        base64_authorization_header = self.extract_base64_authorization_header(
            authorization_header)
        if base64_authorization_header is None:
            return None

        decoded_base64_authorization_header = (
            self.decode_base64_authorization_header(
                base64_authorization_header)
        )
        if decoded_base64_authorization_header is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(
            decoded_base64_authorization_header)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
