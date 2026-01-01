from core import logger
import csv
import os
from .consts import CSV_PATH, CSV_FIELDS


def append_listings_to_csv(stories: list[dict], subreddit: str):
    FILE_PATH = f"{CSV_PATH}/{subreddit}/{subreddit}.csv"

    logger.info(f"Appending listings {len(stories)} from {subreddit}.")

    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    file_exists = os.path.isfile(FILE_PATH)

    with open(FILE_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)

        if not file_exists:
            logger.info("No previous csv, writing headers.")
            writer.writeheader()

        for story in stories:
            writer.writerow(story)

    logger.info(f"Successfully appended {len(stories)} from {subreddit}.")
