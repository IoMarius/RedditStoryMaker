import json
from pathlib import Path
import subprocess
from typing import Iterator
from core import logger
from models.reddit import Story
from dataclasses import asdict
import json

from models.tts import AudioWithTimestamps


def _get_audio_duration_ffprobe(mp3_path: Path) -> int:
    """
    Get audio duration in seconds (rounded) using ffprobe.
    """
    mp3_path = str(mp3_path)

    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            mp3_path,
        ],
        capture_output=True,
        text=True,
    )

    if result.stderr:
        logger.error(f'ffprobe failed for "{mp3_path}".\nEx:{result.stderr}')

    if result.stdout:
        data = json.loads(result.stdout)
        duration = float(data["format"]["duration"])
        return int(round(duration))
    else:
        raise RuntimeError(f"ffprobe failed on {mp3_path}: {result.stderr}")


def _save_audio(audio_stream: Iterator[bytes], path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "wb") as f:
        for chunk in audio_stream:
            if chunk:  # sometimes empty chunks appear
                f.write(chunk)


def _save_script(story: Story, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(story), f, ensure_ascii=False, indent=2)


def _save_tts(tts: AudioWithTimestamps, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(tts), f, ensure_ascii=False, indent=2)


def _load_script(path: str) -> Story:
    with open(path, "r", encoding="utf-8") as f:
        return Story(**(json.load(f)))
