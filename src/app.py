from core.logger import logger
import bot

def main():
    bootstrap()
    logger.info("App started.")

    bot.run_bot()    

def bootstrap():
    from core.listings import (
        run_fetch_stories_pipeline,
        get_subreddits,
        has_unused_listings,
    )

    logger.info("Bootstrapping...")
    subs = get_subreddits()
    
    logger.info("Verifying if local stories are available.")
    for sub in subs:
        if not has_unused_listings(sub.name):
            logger.warning(f"{sub.name} used up all stories. Fetching new stories.")
            run_fetch_stories_pipeline(sub)

    logger.info("Local stories verified.")

if __name__ == "__main__":
    main()