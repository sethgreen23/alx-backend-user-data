#!/usr/bin/env python3
"""
Filtered logger
"""
import re
from typing import List
import logging
import os
import mysql.connector
from dotenv import load_dotenv
load_dotenv()


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Init method for RedactingFormatter class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format a log message"""
        message = logging.Formatter(self.FORMAT).format(record)
        return filter_datum(self.fields,
                            self.REDACTION,
                            message,
                            self.SEPARATOR)


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    Returns the log message obfuscated"""
    for field in fields:
        message = re.sub(
            rf'({re.escape(field)}=)[^{re.escape(separator)}]*',
            r'\1' + redaction,
            message)
    return message


def get_logger() -> logging.Logger:
    """Return Logging Object"""
    logger = logging.getLogger('user_data')
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Get database connector"""
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    database = os.environ.get('PERSONAL_DATA_DB_NAME')
    print(f"PERSONAL_DATA_DB_USERNAME={username}", end=" ")
    print(f"PERSONAL_DATA_DB_PASSWORD={password}", end=" ")
    print(f"PERSONAL_DATA_DB_HOST={host}", end=" ")
    print(f"PERSONAL_DATA_DB_NAME={database}", end=" ")
    return mysql.connector.connect(
        host=os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.environ.get('PERSONAL_DATA_DB_NAME'),
        user=os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    )
