#!/usr/bin/env python3
""" user_session module
"""
from datetime import datetime
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid
from models.base import Base


class UserSession(Base):
    """UserSession class"""
    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a UserSession instance """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
