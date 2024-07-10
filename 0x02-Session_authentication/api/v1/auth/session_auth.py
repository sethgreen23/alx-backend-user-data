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
