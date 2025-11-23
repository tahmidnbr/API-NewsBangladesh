# config.py

NEWS_SITES = [
    {
        "source": "The Business Standard",
        "base_url": "https://www.tbsnews.net",
        "url": "https://www.tbsnews.net/latest",
        "container": "div.card",
        "title": "div.card-section h3",
        "link": "div.card-section a",
        "image": "div.card-image img",
        "time": "div.card-section div.date",
        "time_type": "relative",
        "image_type": "normal",
    },
    {
        "source": "Dhaka Tribune",
        "base_url": "https://www.dhakatribune.com",
        "url": "https://www.dhakatribune.com/bangladesh/nation",
        "container": "div.each",
        "title": "div.info h2.title a.link_overlay",
        "link": "div.info h2.title a.link_overlay",
        "image": "div.image span[id^='ari-image-']",
        "time": "div.additional span.time",
        "time_type": "absolute",
        "image_type": "data-ari",
    }
]
