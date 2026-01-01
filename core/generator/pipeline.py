from pathlib import Path
from typing import Callable
from core import logger
from core.formatter import ai
from core.thumbnail import generate_cover, generate_cover_async
from core.listings import get_best_unused_story, mark_story_scraped
from core.text_to_speech import convert_to_speech_timestamped
from core.video import save_random_segment, generate_reel, test_cover_on_video
from models.reddit import PipelineResult, Story
from .consts import DATA_PATH
from .utils import _save_audio, _save_script, _get_audio_duration_ffprobe

Callback = Callable[[str], None]


def run_generation_pipeline(sub_name: str, callback: Callback) -> None:
    try:
        _run_pipeline(sub_name, callback)
    except Exception as e:
        logger.error("Pipeline failed.", exc_info=True)
        raise


async def run_generation_pipeline_async(
    sub_name: str, callback: Callback
) -> PipelineResult:
    try:
        video_path, story = await _run_pipeline_async(sub_name, callback)
        return PipelineResult(
            video_path=video_path, caption=story.caption, hashtags=story.hashtags
        )

    except Exception as e:
        logger.error("Pipeline failed.", exc_info=True)
        raise


def _run_pipeline(sub_name: str, callback: Callback) -> None:
    raw_story = get_best_unused_story(sub_name)
    callback("📥 Fetched a new story!")

    # Base folder
    story_folder = Path(f"{DATA_PATH}/{sub_name}/{raw_story.id}")
    # story_folder = Path(f"{DATA_PATH}/{sub_name}/1pw9hgm")
    story_folder.mkdir(parents=True, exist_ok=True)

    script_path = story_folder / f"script.json"
    cover_path = story_folder / f"cover.png"
    audio_path = story_folder / f"voice.mp3"
    video_path = story_folder / f"background.mp4"
    final_output = story_folder / f"video.mp4"

    # test_cover_on_video(video_path, audio_path, cover_path, final_output)

    # return
    logger.info(f"{raw_story.id} | Formatting story.")
    callback("✍️ Formatting story...")
    story = ai.format_story(raw_story)
    logger.info(f"{story.id} | Story formatted successfully.")

    callback("🖼 Generating cover image...")
    generate_cover(story, sub_name, cover_path)

    _save_script(story=story, path=script_path)
    callback("📄 Script saved!")

    logger.info(f"{story.id} | Script saved: {script_path}")

    callback("🎤 Converting story to speech...")
    tts_response = convert_to_speech_timestamped(story)
    logger.info(f"{story.id} | Successfully converted story to speech")
    # _save_tts(tts=tts_response, path=tts_path)

    _save_audio(audio_stream=tts_response.audio, path=audio_path)
    logger.info(f"{story.id} | Audio saved: {audio_path}")

    story_duration_s = _get_audio_duration_ffprobe(mp3_path=audio_path)
    save_random_segment(video_path, desired_length=story_duration_s)
    logger.info(f"{story.id} | Successfully cropped story background video")

    logger.info(f"{story.id} | Creating reel video.")
    callback("🎬 Creating video...")
    generate_reel(
        audio_with_timestamps=tts_response,
        video_path=video_path,
        audio_path=audio_path,
        cover_path=cover_path,
        output_path=final_output,
    )

    callback("🏆 Video created successfully!")
    logger.info(f"{story.id} | Successfully created reel.")

    mark_story_scraped(sub_name, story.id)
    logger.info(f"{story.id} | Marked as scraped.")


async def _run_pipeline_async(sub_name: str, callback: Callback) -> tuple[Path, Story]:
    raw_story = get_best_unused_story(sub_name)
    await callback("📥 Fetched a new story!")

    # Base folder
    story_folder = Path(f"{DATA_PATH}/{sub_name}/{raw_story.id}")
    # story_folder = Path(f"{DATA_PATH}/{sub_name}/1pw9hgm")
    story_folder.mkdir(parents=True, exist_ok=True)

    script_path = story_folder / f"script.json"
    cover_path = story_folder / f"cover.png"
    audio_path = story_folder / f"voice.mp3"
    video_path = story_folder / f"background.mp4"
    final_output = story_folder / f"video.mp4"

    # test_cover_on_video(video_path, audio_path, cover_path, final_output)

    # return
    logger.info(f"{raw_story.id} | Formatting story.")
    await callback("✍️ Formatting story...")
    story = ai.format_story(raw_story)
    logger.info(f"{story.id} | Story formatted successfully.")

    await callback("🖼 Generating cover image...")
    await generate_cover_async(story, sub_name, cover_path)

    _save_script(story=story, path=script_path)
    await callback("📄 Script saved!")

    logger.info(f"{story.id} | Script saved: {script_path}")

    await callback("🎤 Converting story to speech...")
    tts_response = convert_to_speech_timestamped(story)
    logger.info(f"{story.id} | Successfully converted story to speech")
    # _save_tts(tts=tts_response, path=tts_path)

    _save_audio(audio_stream=tts_response.audio, path=audio_path)
    logger.info(f"{story.id} | Audio saved: {audio_path}")

    await callback("🧠 Searching for brainrot background video...")
    story_duration_s = _get_audio_duration_ffprobe(mp3_path=audio_path)
    save_random_segment(video_path, desired_length=story_duration_s)
    logger.info(f"{story.id} | Successfully cropped story background video")

    logger.info(f"{story.id} | Creating reel video.")
    await callback("🎬 Creating video...")
    generate_reel(
        audio_with_timestamps=tts_response,
        video_path=video_path,
        audio_path=audio_path,
        cover_path=cover_path,
        output_path=final_output,
    )

    await callback("🏆 Video created successfully!")
    logger.info(f"{story.id} | Successfully created reel.")

    mark_story_scraped(sub_name, story.id)
    logger.info(f"{story.id} | Marked as scraped.")

    return final_output, story
