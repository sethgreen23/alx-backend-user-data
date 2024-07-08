#!/usr/bin/env python3
""" Basic Auth module"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """Basic Auth class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract base64 authorization header"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ Decode base64 authorization header"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            base64.b64decode(base64_authorization_header)
        except Exception:
            return None
        decoded_bytes = base64.b64decode(base64_authorization_header)
        return decoded_bytes.decode('utf-8')

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ Extract user credentials"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if decoded_base64_authorization_header.index(':') == -1:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))
