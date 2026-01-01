from core import logger

def parse_listing(json_data: dict):
    listing = json_data.get("data", {})
    after = listing.get("after")

    logger.info(f"Parsing listings on page {after}")

    stories = []

    for child in listing.get("children", []):
        if child.get("kind") != "t3":
            continue

        d = child.get("data", {})

        body = d.get("selftext", "").strip()
        body = "\n\n".join(p.strip() for p in body.split("\n\n") if p.strip())

        stories.append(
            {
                "id": d.get("id"),
                "subreddit": d.get("subreddit"),
                "title": d.get("title"),
                "body": body,
                "author": d.get("author"),
                "score": d.get("score"),
                "created_utc": d.get("created_utc"),
                "source_url": d.get("url"),
                "used": 0,
            }
        )

    logger.info(f"Parsed {len(stories)} listings.")

    return stories, after
