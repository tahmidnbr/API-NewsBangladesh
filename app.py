from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from config import NEWS_SITES
from scraper.sites import scrape_site

app = Flask(__name__)
all_news = []


def fetch_news():
    global all_news
    collected = []

    print("Fetching news...")

    for site in NEWS_SITES:
        print(f"Scraping: {site['source']}")
        try:
            collected += scrape_site(site)
        except Exception as e:
            print("ERROR:", e)

    all_news = collected
    print(f"Updated: {len(all_news)} articles")


@app.route("/news")
def show_news():
    global all_news

    limit = request.args.get("limit")
    limit = int(limit) if limit and limit.isdigit() else len(all_news)

    # Group by source
    grouped = {}
    for item in all_news:
        grouped.setdefault(item["source"], []).append(item)

    iterators = {src: iter(items) for src, items in grouped.items()}
    sources = list(iterators.keys())

    mixed = []
    index = 0

    while sources and len(mixed) < limit:
        src = sources[index]

        try:
            mixed.append(next(iterators[src]))
            index = (index + 1) % len(sources)
        except StopIteration:
            del iterators[src]
            sources.remove(src)

            if sources:
                index = index % len(sources)

    return jsonify(mixed)


if __name__ == "__main__":
    fetch_news()
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_news, "interval", minutes=1)
    scheduler.start()

    app.run(debug=True, use_reloader=False)
