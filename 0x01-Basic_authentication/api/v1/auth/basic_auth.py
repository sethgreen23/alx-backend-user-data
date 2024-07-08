#!/usr/bin/env python3
""" Basic Auth module"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
from models.user import User
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
        index = decoded_base64_authorization_header.find(':')
        if index == -1:
            return (None, None)
        credentials = decoded_base64_authorization_header.split(':', 1)
        return (credentials[0], credentials[1]) if isinstance(
            credentials, list) else (None, None)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password"""
        if not user_email or not isinstance(user_email, str)\
           or not user_pwd or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        base64_auth = self.extract_base64_authorization_header(auth_header)
        if not base64_auth:
            return None
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if not decoded_auth:
            return None
        user_creds = self.extract_user_credentials(decoded_auth)
        if not user_creds:
            return None
        user_email, usr_pwd = user_creds
        user = self.user_object_from_credentials(user_email, usr_pwd)
        if not user:
            return None
        return user
