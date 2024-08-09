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

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to check if authentication is required for given path
        """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        path = path if path.endswith('/') else path + '/'

        for excluded_path in excluded_paths:
            excluded_path = excluded_path if excluded_path.endswith(
                '/') else excluded_path + '/'
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
