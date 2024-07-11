#!/usr/bin/env python3
""" Session Auth module"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """Class Session Auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create session"""
        if not user_id or not isinstance(user_id, str):
            return None
        id = str(uuid4())
        self.user_id_by_session_id[id] = user_id
        return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ User id for session id"""
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user"""
        try:
            from models.user import User
            session_id = self.session_cookie(request)
            if not session_id:
                return None
            user_id = self.user_id_for_session_id(session_id)
            if not user_id:
                return None
            return User.get(user_id)
        except Exception:
            return None
