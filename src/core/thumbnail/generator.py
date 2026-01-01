from pathlib import Path
import random
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from .consts import HTML_FILE_PATH, COVER_ID
from models.reddit import Story
from core import logger


async def generate_cover_async(
    story: Story, subreddit_name: str, output_path: str
) -> None:
    updates = {
        "subreddit-name": f"r/{subreddit_name}",
        "post-title": story.hook,
        "post-text": _trim_body(story.content, 150),
        "comments-count": random.randint(250, 999),
        "upvotes-count": f"{round(random.uniform(1, 20),1)}K",
    }

    html_file = Path(HTML_FILE_PATH).resolve()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": 1080, "height": 1920}, device_scale_factor=2
        )

        await page.goto(f"file://{html_file}")

        await page.wait_for_load_state("domcontentloaded")
        for element_id, text in updates.items():
            await page.eval_on_selector(f"#{element_id}", f"el=>el.innerText = `{text}`")
        logger.info(f"Updated template cover for story {story.id}.")

        await page.wait_for_timeout(200)

        cover_element = await page.query_selector(f"#{COVER_ID}")
        await cover_element.screenshot(path=output_path, omit_background=True)
        logger.info(f"Took screenshot of element for {story.id}.")

        await browser.close()


def generate_cover(story: Story, subreddit_name: str, output_path: str) -> None:
    updates = {
        "subreddit-name": f"r/{subreddit_name}",
        "post-title": story.hook,
        "post-text": _trim_body(story.content, 150),
        "comments-count": random.randint(250, 999),
        "upvotes-count": f"{round(random.uniform(1, 20),1)}K",
    }

    html_file = Path(HTML_FILE_PATH).resolve()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1080, "height": 1920}, device_scale_factor=2
        )

        page.goto(f"file://{html_file}")

        page.wait_for_load_state("domcontentloaded")
        for element_id, text in updates.items():
            page.eval_on_selector(f"#{element_id}", f"el=>el.innerText = `{text}`")
        logger.info(f"Updated template cover for story {story.id}.")

        page.wait_for_timeout(200)

        cover_element = page.query_selector(f"#{COVER_ID}")
        cover_element.screenshot(path=output_path, omit_background=True)
        logger.info(f"Took screenshot of element for {story.id}.")

        browser.close()


def _trim_body(str: str, length: int) -> str:
    return (str[:length] + ("..." if len(str) > length else ""),)
