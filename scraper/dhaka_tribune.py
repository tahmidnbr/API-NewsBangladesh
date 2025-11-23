# scraper/dhaka_tribune.py

from datetime import datetime
from bs4 import BeautifulSoup
import requests

def fetch_dt_timestamp(url: str):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        tag = soup.select_one("span.modified_time[itemprop='dateModified']")
        if tag and tag.get("content"):
            return datetime.fromisoformat(tag["content"])
    except:
        pass
    return None
