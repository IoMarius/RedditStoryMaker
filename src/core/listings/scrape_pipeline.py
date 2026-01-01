import requests
from core import logger
from models.reddit import Subreddit
from ..listings import (
    append_listings_to_csv,
    parse_listing,
    save_scrape_state,
    load_scrape_state,
)
import random
import time


def run_fetch_stories_pipeline(sub: Subreddit):
    logger.info(f"Running listings pipeline for r/{sub.name}.")
    last_state = load_scrape_state(sub.name)

    if last_state:
        sub.url = f"{sub.url}?after={last_state}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
    }

    response = requests.get(url=sub.url, headers=headers)
    
    fail_count = 0
    if not response.ok:
        if fail_count == 3:
            raise Exception(f"Cannot fetch data for r/{sub.name}.")
        logger.error(
            f"Failed to fetch from r/{sub.name}. \nStatus code {response.status_code} Url: {sub.url}."
        )
        fail_count += 1
        time.sleep(round(random.uniform(2, 6), 2))
        return run_fetch_stories_pipeline(sub)

    json_data = response.json()

    stories, after = parse_listing(json_data)

    if stories:
        append_listings_to_csv(stories, subreddit=sub.name)

    if after:
        save_scrape_state(subreddit=sub.name, after=after)

    logger.info(f"Listings pipeline ran successfully for r/{sub.name}")
