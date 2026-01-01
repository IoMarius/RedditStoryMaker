import json
import os

STATE_PATH = "./data/scrape_state.json"


def load_scrape_state(subreddit: str):
    """
    Returns the last 'after' value for a specific subreddit.
    """
    if not os.path.isfile(STATE_PATH):
        return None

    with open(STATE_PATH, "r", encoding="utf-8") as f:
        try:
            states = json.load(f)
        except json.JSONDecodeError:
            return None

    for state in states:
        if state.get("subreddit") == subreddit:
            return state.get("after")

    return None


def save_scrape_state(subreddit: str, after: str):
    """
    Saves or updates the 'after' value for a specific subreddit.
    """
    states = []

    if os.path.isfile(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            try:
                states = json.load(f)
            except json.JSONDecodeError:
                states = []

    # Check if subreddit already exists
    for state in states:
        if state.get("subreddit") == subreddit:
            state["after"] = after
            break
    else:
        # Not found, append new
        states.append({"subreddit": subreddit, "after": after})

    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(states, f, indent=2)
        
def mark_story_scraped(subreddit: str, story_id: str):
    """
    Adds a story ID to the 'scraped' list for a subreddit.
    Creates the subreddit entry if it doesn't exist.
    """
    states = []

    if os.path.isfile(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            try:
                states = json.load(f)
            except json.JSONDecodeError:
                states = []

    # Find subreddit state
    for state in states:
        if state.get("subreddit") == subreddit:
            scraped = state.setdefault("scraped", [])
            if story_id not in scraped:
                scraped.append(story_id)
            break
    else:
        # Subreddit not found, create new entry
        states.append({"subreddit": subreddit, "after": None, "scraped": [story_id]})

    # Save back
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(states, f, indent=2)

