#!/usr/bin/env python3
"""Regex-ing"""
import logging
from typing import List
import re


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns obfuscated log message"""
    fields = "|".join(fields)
    res = re.sub(r'({})=.*?{}'.format(fields, separator),
                 rf"\1={redaction}{separator}", message)
    return res


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialization"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Implement the format method to filter values in
        incoming log records using filter_datum"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Returns logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    s_hdlr = logging.StreamHandler()
    logger.addHandler(s_hdlr)
    formatter = RedactingFormatter(list(PII_FIELDS))
    s_hdlr.setFormatter(formatter)
    return logger
