import json
import os
from typing import Any
from core import logger
from dotenv import load_dotenv
from openai import OpenAI

from models.reddit import RawStory, Story
from .prompts import get_sys_prompt
from .consts import FORMAT_STORY_PROMPT_V2, FORMAT_STORY_PROMPT_V1

load_dotenv()

GPT_MODEL = os.getenv("GPT_MODEL")
GPT_API_KEY = os.getenv("GPT_API_KEY")

client = OpenAI(api_key=GPT_API_KEY)


def format_story(story: RawStory) -> Story:
    raw_json = _make_request(
        prompt=f"Id: {story.id}.Title:{story.title}\nStory:{story.body}",
        system_prompt_keyword=FORMAT_STORY_PROMPT_V1,
    )

    try:
        data: dict[str, Any] = json.loads(raw_json)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse GPT response as JSON", raw_json, e)
        raise

    for field in ["hook", "content", "conclusion", "caption", "hashtags"]:
        if field not in data or not isinstance(data[field], str):
            raise ValueError(
                f"Missing or invalid field '{field}' in GPT response: {data}"
            )

    formatted = Story(
        id=story.id,
        hook=data["hook"],
        content=data["content"],
        conclusion=data["conclusion"],
        caption=data["caption"],
        hashtags=data["hashtags"]
    )

    return formatted


def _make_request(prompt, system_prompt_keyword) -> str:
    system_prompt = get_sys_prompt(system_prompt_keyword)
    logger.debug(f"Sending request to {GPT_MODEL}. Using {system_prompt_keyword}.")
    response = client.chat.completions.create(
        model=GPT_MODEL,
        response_format={"type": "json_object"},
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )
    logger.debug(f"Response received from {GPT_MODEL} to {system_prompt_keyword}.")

    return response.choices[0].message.content
