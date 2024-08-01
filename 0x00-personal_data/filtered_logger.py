#!/usr/bin/env python3
"""
Filtered logger
"""

import logging
import mysql.connector
import os
import re
from typing import List


PII_FIELDS = ("name", "email", "ssn", "password", "phone")


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """
    Obfuscates the specified fields in a log message
    """
    pattern = r'({})=[^{}]*'.format('|'.join(re.escape(field)
                                             for field in fields),
                                    re.escape(separator))
    return re.sub(
        pattern,
        lambda m: f"{m.group().split('=')[0]}={redaction}",
        message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter Class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize formatter with specified fields to redact
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formaat the log record, filtering sensitive data
        """
        original_message = super(RedactingFormatter, self).format(record)
        return filter_datum(
            self.fields,
            self.REDACTION,
            original_message,
            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Creates a logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connects to the database using credentials
    from environment variables
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
    )
