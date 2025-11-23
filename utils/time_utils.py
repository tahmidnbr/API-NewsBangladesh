# utils/time_utils.py

from datetime import datetime, timedelta
import re

def parse_relative_time(text: str) -> datetime:
    now = datetime.now()
    text = text.lower().strip()

    match = re.match(r"(\d+)\s*(h|hr|hrs|m|min|d|day|days) ago", text)
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
