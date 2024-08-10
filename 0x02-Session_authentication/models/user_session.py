#!/usr/bin/env python3
"""
UserSession model
"""
from models.base import Base
from uuid import uuid4
from datetime import datetime

class UserSession(Base):
    """
    UserSession class that inherits from Base
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize a UserSession
        """
        if len(kwargs) != 2:
            raise TypeError('Invalid number of arguments')
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
        self.created_at = datetime.now()
        super().__init__(*args, **kwargs)
