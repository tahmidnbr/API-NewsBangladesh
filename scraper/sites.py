# scraper/sites.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from scraper.parser import extract_image, extract_time

def scrape_site(site):
    articles = []
    
    try:
        res = requests.get(site["url"], timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        blocks = soup.select(site["container"])

        for block in blocks:
            title_tag = block.select_one(site["title"])
            link_tag = block.select_one(site["link"])

            if not title_tag or not link_tag:
                continue

            title = title_tag.get_text(strip=True)
            link = urljoin(site["base_url"], link_tag.get("href"))

            img = extract_image(block, site)
            time_val = extract_time(block, site, link)

            articles.append({
                "title": title,
                "link": link,
                "source": site["source"],
                "image": img or "N/A",
                "time": time_val.isoformat() if time_val else "N/A",
            })

    except Exception as e:
        print(f"[ERROR] {site['source']}: {e}")

    return articles
