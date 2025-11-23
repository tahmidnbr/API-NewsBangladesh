# scraper/parser.py

import json
import html
from urllib.parse import urljoin
from utils.time_utils import parse_relative_time
from scraper.dhaka_tribune import fetch_dt_timestamp

def extract_image(container, site):
    tag = container.select_one(site["image"])
    if not tag:
        return None

    # Dhaka Tribune style JSON inside data-ari
    if site["image_type"] == "data-ari":
        data_ari = tag.get("data-ari")
        if not data_ari:
            return None

        try:
            data = json.loads(html.unescape(data_ari))
            path = data.get("path")
            if not path:
                return None

            if path.startswith("media/"):
                return "https://ecdn.dhakatribune.net/" + path
            if path.startswith("//"):
                return "https:" + path
            if path.startswith("/"):
                return "https://ecdn.dhakatribune.net" + path
        except:
            return None

    # Normal image attributes
    for attr in ["src", "data-src", "data-lazy-src"]:
        img = tag.get(attr)
        if img:
            if img.startswith("//"):
                return "https:" + img
            return urljoin(site["base_url"], img)

    return None


def extract_time(container, site, link):
    tag = container.select_one(site["time"])

    if site["time_type"] == "absolute" and link:
        return fetch_dt_timestamp(link)

    if site["time_type"] == "relative" and tag:
        return parse_relative_time(tag.get_text(strip=True))

    return None
