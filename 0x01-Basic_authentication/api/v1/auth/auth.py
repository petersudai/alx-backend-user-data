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
        Method that returns False. This method will be used later.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Method that returns None. This method will be used later.
        """
        return None

    def current_user(self, request=None) -> User:
        """
        Method that returns None. This method will be used later.
        """
        return None
