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

    if site.get("image_type") == "data-ari":
        data_ari = tag.get("data-ari")
        if data_ari:
            try:
                data = json.loads(html.unescape(data_ari))
                path = data.get("path")
                if path:
                    # Full URL already
                    if path.startswith("http://") or path.startswith("https://"):
                        return path
                    if path.startswith("//"):
                        return "https:" + path
                    # If path starts with 'media/', prepend contents/cache/images/1100x618x1/uploads/
                    if path.startswith("media/"):
                        path = "contents/cache/images/1100x618x1/uploads/" + path
                    # Join with base URL
                    return urljoin(site["base_url"], path)
            except json.JSONDecodeError:
                return None


def extract_time(container, site, link):
    tag = container.select_one(site["time"])

    if site["time_type"] == "absolute" and link:
        return fetch_dt_timestamp(link)

    if site["time_type"] == "relative" and tag:
        return parse_relative_time(tag.get_text(strip=True))

    return None
