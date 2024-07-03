#!/usr/bin/env python3
"""
Filtered logger
"""
import re


def filter_datum(fields: list,
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    Returns the log message obfuscated"""
    new_message = message
    for field in fields:
        pattern = rf'({re.escape(field)}=)[^{re.escape(separator)}]*'
        new_message = re.sub(pattern, r'\1' + redaction, new_message)
    return new_message
