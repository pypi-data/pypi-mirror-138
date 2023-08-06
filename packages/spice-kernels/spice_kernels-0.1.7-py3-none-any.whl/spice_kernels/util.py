"""
Miscellaneous utilities.
"""
from datetime import datetime, timedelta
from dateutil import parser


def mid_time(start: datetime, end: datetime) -> datetime:
    """
    Get the mid-point between two times.

    :param start: time
    :param end: time
    :return: mid-point time
    """
    half_seconds = (end - start).total_seconds() / 2
    return start + timedelta(seconds=half_seconds)


def from_utc(utc: str) -> datetime:
    """
    Get a datetime from a UTC string.
    :param utc: string
    :return: datetime
    """
    return parser.parse(utc)
