#!/usr/bin/env python3
"""
Encrypt password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Hash a password """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Valid password"""
    input_password = password.encode('utf-8')
    return bcrypt.checkpw(input_password, hashed_password)
