![alt text](header.png)

# StoryMaker
Automatic reddit storytelling video generator.

## Overview
StoryMaker takes Reddit content and produces short storytelling videos by combining generated narration, thumbnails, and background footage. It is split into a lightweight bot interface and a core generation pipeline (formatting, TTS, thumbnailing, and video composition).

## Architecture (brief)
- **Bot**: `src/bot` — Telegram command interface and dispatching.
- **Core pipeline**: `src/core` — contains formatter (LLM prompts), generator pipeline, text-to-speech, thumbnail generator, and video manager.
- **Models**: `src/models` — provider-specific wrappers (e.g., Reddit fetch, TTS models).
- **Data / assets**: `data/assets` — fonts, HTML templates, prompts, and background videos used for composition.

## Environment variables
The project uses `python-dotenv` and reads a `.env` file when present. Important environment variables:

- `TELEGRAM_BOT_TOKEN`: (optional) Telegram bot token for controlling the bot.
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

Note: If a variable is not set the corresponding feature may be disabled or fall back to defaults; consult the relevant module in `src/` for details.

## Volumes / where to put background videos
When running in Docker or with a mounted data directory, the container expects a data mount at `/app/data`. On the host, create the corresponding folder and the `assets/video/` subfolder where MP4 background videos must be placed.

- Host path example: `./data/assets/video/`
- Container path: `/app/data/assets/video/`

Put MP4 files in that `assets/video/` folder. Videos used as backgrounds work best when they are long gameplay or continuous-motion clips (recommended: Subway Surfers or Minecraft gameplay videos, ~20–30 minutes). These long clips provide many unique frames for background generation and reduce visible repetition.

Files should be plain MP4s; the pipeline will pick videos from this folder when composing backgrounds.

## Notes
- Playwright is installed in the Dockerfile for any browser-based interactions.
- The Dockerfile installs system libraries used for multimedia processing and fonts.
- If you plan to run locally without Docker, ensure the same system libraries and `playwright` are installed and that `PYTHONPATH` includes the project root or use the project as a package.

## Where to look in the code
- Bot entry: `src/bot/bot.py`
- Formatter / prompts: `src/core/formatter`
- TTS conversion: `src/core/text_to_speech`
- Video composition: `src/core/video` and `src/core/video/video_manager.py`

If you want, I can also add a short run section with Docker Compose examples and exact mount commands.
