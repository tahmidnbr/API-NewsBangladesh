# scraper/sites.py
# checks the suce andd sends to the correct parser

from scraper.common_parser import parse_common_site
from scraper.dhaka_tribune_parser import parse_dhaka_tribune

def scrape_site(site):
    if site["source"] == "Dhaka Tribune":
        return parse_dhaka_tribune(site)
    else:
        return parse_common_site(site)
