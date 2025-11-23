# scraper/common_parser.py

import requests
from bs4 import BeautifulSoup
from utils.time_utils import parse_relative_time
from urllib.parse import urljoin
from scraper.header import HEADERS

def parse_common_site(site):
    news = []

    response = requests.get(site["url"], headers=HEADERS, timeout=10)
    response.raise_for_status()  # helps debugging

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select(site["container"])
    for a in articles:
        title_tag = a.select_one(site["title"])

        if not title_tag:
            continue

        link = urljoin(site["base_url"], title_tag.get("href"))
        title = title_tag.get_text(strip=True)

        # image
        img_tag = a.select_one(site["image"])
        img = None
        if img_tag:
            img = img_tag.get("src") or img_tag.get("data-src")
            if img and img.startswith("//"):
                img = "https:" + img

        # time
        time_tag = a.select_one(site["time"])
        published = None
        if time_tag:
            published = parse_relative_time(time_tag.get_text(strip=True))

        news.append({
            "source": site["source"],
            "title": title,
            "link": link,
            "image": img,
            "published": str(published)
        })

    return news
