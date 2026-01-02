from core.path_utils import get_data_path

STATE_PATH = get_data_path("scrape_state.json")
CSV_PATH = get_data_path("stories")
SUBREDDITS_PATH = get_data_path("subreddits.json")
CSV_FIELDS = [
    "id",
    "subreddit",
    "title",
    "body",
    "author",
    "score",
    "created_utc",
    "source_url",
    "used",
]
