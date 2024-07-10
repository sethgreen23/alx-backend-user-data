#!/usr/bin/env python3
""" Auth module"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """ Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require authentication"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        for p in excluded_paths:
            if p[-1] == '*':
                p = p[:-1]
            elif p[-1] != '/':
                p += '/'
            if p in path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header"""
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user"""
        return None
    
    def session_cookie(self, request=None) -> str:
        """ Session cookie"""
        if not request:
            return None
        cookie_name = os.getenv('SESSION_NAME', '_my_session_id') 
        return request.cookies.get(cookie_name)
