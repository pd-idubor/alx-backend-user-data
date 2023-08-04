#!/usr/bin/env python3
"""Regex-ing"""
import logging
from typing import List
import re
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection


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


def get_db() -> MySQLConnection:
    """Returns a connector object to the database"""
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    name = os.getenv("PERSONAL_DATA_DB_NAME")
    db_connector = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        database=name
    )
    return db_connector


def main():
    """Obtain a db connection, retrieve all rows users table and
    display each row under a filtered format"""
    all_PII_FIELDS = ("name", "email", "phone", "ssn",
                      "password", "ip", "last_login", "user_agent")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        infos = "; ".join([f"{all_PII_FIELDS[i]}={row[i]}" for i in range(8)])
        log_record = logging.LogRecord("user_data", logging.INFO,
                                       None, None, infos, None, None)
        formatter = RedactingFormatter(list(PII_FIELDS))
        print(formatter.format(log_record))
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
