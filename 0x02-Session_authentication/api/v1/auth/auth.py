#!/usr/bin/env python3
"""
Auth module for the API
"""
from typing import List, TypeVar
from flask import request


User = TypeVar('User')


class Auth:
    """
    authenticating users
    """

    def require_auth(self, path: str, excluded_paths: list) -> bool:
        """
        Method to check if authentication is required for given path
        """
        if path is None or not excluded_paths:
            return True

        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False

            else:
                if path == excluded_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the Authorization header from the request, if present
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> User:
        """
        Method that returns None. This method will be used later.
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns the value of the session cookie
        """
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME')
        if session_name is None:
            return None

        return request.cookies.get(session_name)
