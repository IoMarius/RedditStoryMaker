# RedditStoryMaker
Automatic reddit storytelling video generator.

## Overview
StoryMaker takes Reddit content and produces short storytelling videos by combining generated narration, thumbnails, and background footage. It is split into a lightweight bot interface and a core generation pipeline (formatting, TTS, thumbnailing, and video composition).

## Environment variables
The project uses `python-dotenv` and reads a `.env` file when present. Important environment variables:

- `TELEGRAM_BOT_TOKEN`: Telegram bot token for controlling the bot.
- `GPT_API_KEY`: API key for your LLM provider (used by the formatter).
- `GPT_MODEL`: Model name to use for text generation (e.g. `gpt-4o-mini` or another supported model).
- `ELEVENLABS_API_KEY`: API key for ElevenLabs (used for TTS, if enabled).
- `ELEVENLABS_MODEL`: ElevenLabs voice/model id to use for TTS.

Example `.env` contents:

TELEGRAM_BOT_TOKEN=xxx
GPT_API_KEY=xxx
GPT_MODEL=gpt-4o-mini
ELEVENLABS_API_KEY=xxx
ELEVENLABS_MODEL=standard_v1

## Volumes / where to put background videos
When running in Docker or with a mounted data directory, the container expects a data mount at `/app/data`. On the host, create the corresponding folder and the `assets/video/` subfolder where MP4 background videos must be placed.

- Host path example: `./data/assets/video/`
- Container path: `/app/data/`

Put MP4 files in that `assets/video/` folder. Videos used as backgrounds work best when they are long gameplay or continuous-motion clips (recommended: Subway Surfers or Minecraft gameplay videos, ~20–30 minutes). These long clips provide many unique frames for background generation and reduce visible repetition.

Files should be plain MP4s; the pipeline will pick videos from this folder when composing backgrounds.

## Notes
- Playwright is installed in the Dockerfile for any browser-based interactions.
- The Dockerfile installs system libraries used for multimedia processing(ffmpeg).
- If you plan to run locally without Docker, ensure the same system libraries and `playwright` are installed and that `PYTHONPATH` includes the project root or use the project as a package.

## Where to look in the code
- Bot entry: `src/bot/bot.py`
- Post to script: / prompts: `src/core/formatter`
- TTS conversion: `src/core/text_to_speech`
- Video composition: `src/core/video` and `src/core/video/video_manager.py`
- Main pipeline: `src/core/generator/pipeline.py`
