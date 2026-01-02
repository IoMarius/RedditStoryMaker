import json
import os
import csv
from typing import Optional
from core import logger

from models.reddit import RawStory
from .consts import CSV_PATH, SUBREDDITS_PATH, STATE_PATH
from models import Subreddit


def has_unused_listings(sub_name: str) -> bool:
    path = f"{CSV_PATH}/{sub_name}/{sub_name}.csv"

    if not os.path.isfile(path):
        return False

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("used") == "0":
                return True

    return False


def get_subreddits() -> list[Subreddit]:
    logger.info(
        f"Looking for subreddits.json, in: '{os.path.abspath(SUBREDDITS_PATH)}'.\n CWD is {os.getcwd()}."
    )
    
    # with open(SUBREDDITS_PATH, "r", encoding="utf-8") as f:
    #     data = json.load(f)

    subs = []
    for item in data.get("Subs", []):
        name = item.get("Name")
        url = item.get("Url")
        if name and url:
            subs.append(Subreddit(name=name, url=url))

    return subs


def get_best_unused_story(sub_name: str) -> Optional[RawStory]:

    csv_path = f"{CSV_PATH}/{sub_name}/{sub_name}.csv"

    if not os.path.isfile(csv_path):
        return None

    # Load scraped IDs from state
    scraped_ids: set[str] = set()

    if os.path.isfile(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            try:
                states = json.load(f)
            except json.JSONDecodeError:
                states = []

        for state in states:
            if state.get("subreddit") == sub_name:
                scraped_ids = set(state.get("scraped", []))
                break

    top_story = None
    max_score = -1

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            story_id = row.get("id")
            if not story_id:
                continue

            # Skip stories already marked as scraped/used
            if story_id in scraped_ids:
                continue

            try:
                score = int(row.get("score", 0))
            except (TypeError, ValueError):
                score = 0

            if score > max_score:
                max_score = score
                top_story = row

    if not top_story:
        return None

    return RawStory(
        id=top_story["id"],
        title=top_story.get("title", ""),
        body=top_story.get("body", ""),
        score=max_score,
    )
