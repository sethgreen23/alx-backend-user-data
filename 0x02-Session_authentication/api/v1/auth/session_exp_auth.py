#!/usr/bin/env python3
""" Session ExpirationAuth module"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Session Expiration Auth"""
    def __init__(self):
        """ Initialize Session Expiration Auth"""
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """User id for session id"""
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if not session_id or not session_dictionary:
            return None
        created_at = session_dictionary.get('created_at')
        user_id = session_dictionary.get('user_id')
        if self.session_duration <= 0:
            return user_id
        if not created_at:
            return None
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None
        return user_id
