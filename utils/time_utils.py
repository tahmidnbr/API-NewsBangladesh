# utils/time_utils.py

from datetime import datetime, timedelta
import re

def parse_relative_time(text: str) -> datetime:
    """
    Converts strings like '5h ago', '20 mins ago', '3 days ago'
    into proper datetime objects.
    """
    now = datetime.now()
    text = text.lower().strip()

    match = re.match(r"(\d+)\s*(h|hr|hrs|hour|hours|m|min|mins|minute|minutes|d|day|days)\s*ago", text)
    if not match:
        return now

    value, unit = match.groups()
    value = int(value)

    if unit.startswith("h"):
        return now - timedelta(hours=value)
    if unit.startswith("m"):
        return now - timedelta(minutes=value)
    if unit.startswith("d"):
        return now - timedelta(days=value)

    return now
