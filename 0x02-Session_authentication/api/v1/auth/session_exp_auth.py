#!/usr/bin/env python3
"""
Session Database Authentication
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
from typing import Optional


class SessionDBAuth(SessionExpAuth):
    """ Session Database Authentication class """

    def __init__(self):
        """
        Initialize the SessionDBAuth instance
        """
        super().__init__()

    def create_session(self, user_id: Optional[str] = None) -> Optional[str]:
        """
        Create a session and store it in the database
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Store session in the database
        UserSession(user_id=user_id, session_id=session_id).save()
        return session_id

    def user_id_for_session_id(
            self,
            session_id: Optional[str] = None) -> Optional[str]:
        """
        Return the user ID based on session ID considering expiration
        """
        if session_id is None:
            return None

        # Retrieve session from the database
        session = UserSession.find_by_session_id(session_id)
        if session is None:
            return None

        if self.session_duration <= 0:
            return session.user_id

        created_at = session.created_at
        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            self.destroy_session(session_id)
            return None

        return session.user_id

    def destroy_session(self, request=None):
        """
        Destroy the session based on the session ID in the request cookie
        """
        if request is None:
            return

        session_id = self.session_cookie(request)
        if session_id is None:
            return

        UserSession.delete_by_session_id(session_id)
