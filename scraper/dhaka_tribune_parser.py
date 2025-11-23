# scraper/dhaka_tribune_parser.py

import json, html
import requests
from bs4 import BeautifulSoup
from scraper.dhaka_tribune import fetch_dt_timestamp
from scraper.header import HEADERS

def parse_dhaka_tribune(site):
    response = requests.get(site["url"], headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.select(site["container"])
    results = []   # <-- FIX: we need a local list

    for a in articles:
        title_tag = a.select_one(site["title"])
        if not title_tag:
            continue

        # -------- TITLE --------
        title = title_tag.get_text(strip=True)

        # -------- LINK --------
        link = title_tag.get("href")
        if not link:
            continue

        if not link.startswith("http"):
            link = "https://www.dhakatribune.com" + link

        # -------- IMAGE --------
        img = None
        img_tag = a.select_one(site["image"])

        if img_tag:
            data_ari = img_tag.get("data-ari")
            if data_ari:
                try:
                    parsed = json.loads(html.unescape(data_ari))

                    # 1️⃣ Try full cached image (BEST)
                    cache = (
                        parsed.get("contents", {})
                              .get("cache", {})
                              .get("images", [])
                    )

                    if cache and "url" in cache[0]:
                        img = cache[0]["url"]

                    # 2️⃣ fallback to parsed["url"]
                    elif "url" in parsed:
                        img = parsed["url"]

                    # 3️⃣ fallback to path
                    else:
                        p = parsed.get("path")
                        if p:
                            img = "https://ecdn.dhakatribune.net/contents/cache/images/1100x618x1/uploads/" + p

                except Exception as e:
                    print("Error parsing DT image:", e)


        # -------- TIME --------
        published = fetch_dt_timestamp(link)

        results.append({
            "source": site["source"],
            "title": title,
            "link": link,
            "image": img or None,
            "published": published
        })

    return results
