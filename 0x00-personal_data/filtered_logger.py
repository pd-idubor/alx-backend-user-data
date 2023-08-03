#!/usr/bin/env python3
"""Regex-ing"""
import logging
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns obfuscated log message"""
    fields = "|".join(fields)
    res = re.sub(r'({})=.*?{}'.format(fields, separator),
                 rf"\1={redaction}{separator}", message)
    return res
