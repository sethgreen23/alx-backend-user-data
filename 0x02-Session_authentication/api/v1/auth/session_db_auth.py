#!/usr/bin/env python3
""" Session DB Auth module"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.session_exp_auth import SessionExpAuth
from os import getenv
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ Session DB Auth class"""
    def create_session(self, user_id=None):
        """ Create Session DB Auth"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        try:
            from models.user_session import UserSession
            user_session = UserSession({'user_id': user_id,
                                        'session_id': session_id})
            user_session.save()
        except Exception:
            return None
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ User id for session id"""
        try:
            from models.user_session import UserSession
            users = UserSession.search({'session_id': session_id})
            if not users:
                return None
            user_id = users[0].user_id
            return user_id
        except Exception:
            return None

    def destroy_session(self, request=None) -> bool:
        """ Destroy session"""
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        try:
            from models.user_session import UserSession
            user_sessions = UserSession.search({'session_id': session_id})
            if not user_sessions:
                return False
            user_session = user_sessions[0]
            user_session.remove()
            self.user_id_by_session_id.pop(session_id)
            return True
        except Exception:
            return False
