#!/usr/bin/env python3
""" Auth module"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require authentication"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        for p in excluded_paths:
            if p[-1] != '/':
                p += '/'
            if p in path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user"""
        return None
