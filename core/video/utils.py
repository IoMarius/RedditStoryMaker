import tempfile
import subprocess
import json
import random
from pathlib import Path
from typing import Iterator
from .consts import INPUT_FOLDER, VIDEO_EXTENSIONS
from core import logger
from pprint import pprint

def get_random_video_path() -> Path:
    folder = Path(INPUT_FOLDER)

    video_files = [
        f
        for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in VIDEO_EXTENSIONS
    ]

    if not video_files:
        logger.error(
            f"Error: No video files found in '{INPUT_FOLDER}'. Supported formats: {', '.join(sorted(VIDEO_EXTENSIONS))}"
        )
        return None

    selected_video = random.choice(video_files)
    logger.info(
        f'Randomly selected "{selected_video.name}". (from {len(video_files)} video(s) in folder)'
    )

    return selected_video


def get_crop_dimensions(video_width, video_height):
    """
    Calculate crop dimensions for 9:16 mobile aspect ratio (center crop),
    ensuring width and height are divisible by 2.
    """
    target_aspect = 9 / 16  # Mobile aspect ratio (width/height)
    current_aspect = video_width / video_height

    if current_aspect > target_aspect:
        # Video is wider than target - crop sides
        new_width = int(video_height * target_aspect)
        new_height = video_height
        x_center = video_width / 2
        y_center = video_height / 2
        x1 = int(x_center - new_width / 2)
        y1 = 0
        x2 = int(x_center + new_width / 2)
        y2 = new_height
    else:
        # Video is taller than target - crop top/bottom
        new_width = video_width
        new_height = int(video_width / target_aspect)
        x_center = video_width / 2
        y_center = video_height / 2
        x1 = 0
        y1 = int(y_center - new_height / 2)
        x2 = new_width
        y2 = int(y_center + new_height / 2)

    # --- Force even numbers ---
    x1, y1, x2, y2 = map(lambda v: v // 2 * 2, (x1, y1, x2, y2))

    return x1, y1, x2, y2

