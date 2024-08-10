#!/usr/bin/env python3
"""
SessionDBAuth authentication system
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class that inherits from SessionExpAuth
    """

    def create_session(self, user_id=None):
        """
        Create a new session in the database
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()  # Save to file-based database
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Get user ID from session ID
        """
        if session_id is None:
            return None
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return None
        user_session = user_session[0]
        if self.session_duration > 0:
            if user_session.created_at + \
                    timedelta(seconds=self.session_duration) < datetime.now():
                return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """
        Destroy the user session
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return False
        user_session = user_session[0]
        user_session.remove()  # Remove from file-based database
        return True
