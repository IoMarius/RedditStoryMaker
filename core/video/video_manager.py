from moviepy import AudioClip
from core import logger
import random
from pathlib import Path
from moviepy import (
    TextClip,
    ImageClip,
    VideoClip,
    VideoFileClip,
    AudioFileClip,
    CompositeVideoClip,
)
from moviepy.video.fx.Crop import Crop
from PIL import Image, ImageDraw
import numpy as np

from .utils import get_crop_dimensions, get_random_video_path
from .consts import FONT_BANGERS_REGULAR


def test_cover_on_video(
    video_path: str, audio_path: str, cover_path: str, output_path: str
):
    # --- Load the base video ---
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    cover_duration = 2  # seconds
    fade_duration = 0.3  # seconds

    # --- Load and prepare the cover image ---
    cover_clip = (
        ImageClip(cover_path)
        .resized(width=int(video_clip.w * 0.8))
        .with_duration(cover_duration)
        .with_position(("center", "center"))
    )

    # Create rounded corners mask
    def create_rounded_mask(size, radius):
        """Create a mask with rounded corners"""
        width, height = size
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)

        # Draw rounded rectangle
        draw.rounded_rectangle([(0, 0), (width, height)], radius=radius, fill=255)

        return np.array(mask) / 255.0  # Convert to 0.0-1.0 range

    # Create base rounded corner mask
    corner_radius = 15  # Adjust this value for more/less rounding
    rounded_mask_base = create_rounded_mask((cover_clip.w, cover_clip.h), corner_radius)

    # Create a mask that fades and has rounded corners
    def make_frame_mask(t):
        if t < cover_duration - fade_duration:
            # Fully opaque for first 2 seconds
            opacity = 1.0
        else:

            progress = (t - (cover_duration - fade_duration)) / fade_duration
            opacity = 1.0 - progress  # goes from 1.0 to 0.0

        # Apply both rounded corners and fade
        return rounded_mask_base * opacity

    # Create the mask clip
    mask_clip = VideoClip(is_mask=True)
    mask_clip.get_frame = make_frame_mask
    mask_clip.duration = cover_duration
    mask_clip.size = (cover_clip.w, cover_clip.h)

    # Apply the mask to the cover
    cover_clip = cover_clip.with_mask(mask_clip)

    # --- Simple placeholder text clip ---
    text_clip = (
        TextClip(
            text="Sample Text",
            font_size=50,
            color="white",
            font=FONT_BANGERS_REGULAR,
            method="caption",
            size=(int(video_clip.w * 0.9), int(video_clip.h * 0.3)),
            stroke_color="black",
            stroke_width=2,
        )
        .with_duration(video_clip.duration)  # full video duration
        .with_position(("center", "center"))  # near bottom
    )

    # --- Compose video + cover + text ---
    final_clip = CompositeVideoClip(
        [video_clip, text_clip, cover_clip], size=video_clip.size
    ).with_audio(audio_clip)

    # --- Write output ---
    final_clip.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        audio_bitrate="128k",
        ffmpeg_params=[
            "-pix_fmt",
            "yuv420p",
            "-profile:v",
            "baseline",
            "-level",
            "3.0",
            "-movflags",
            "+faststart",
        ],
    )


def generate_reel(
    audio_with_timestamps,
    video_path: str,
    audio_path: str,
    cover_path: str,
    output_path: str,
    cover_time_seconds: int = 3,
    target_fps: int = 30,
    font_path: str = FONT_BANGERS_REGULAR,
):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    words = audio_with_timestamps.words()

    text_clips = []
    for word in words:
        txt_clip = (
            TextClip(
                text=word.text,
                font_size=65,
                color="white",
                font=font_path,
                method="caption",
                size=(int(video_clip.w * 0.9), int(video_clip.h * 0.3)),
                stroke_color="black",
                stroke_width=2,
            )
            .with_start(word.start)
            .with_duration(word.end - word.start)
            .with_position(("center", "center"))
        )
        text_clips.append(txt_clip)

    cover_duration = 2  # seconds
    fade_duration = 0.3  # seconds

    cover_clip = (
        ImageClip(cover_path)
        .resized(width=int(video_clip.w * 0.8))
        .with_duration(cover_duration)
        .with_position(("center", "center"))
    )

    # Create rounded corners mask
    def create_rounded_mask(size, radius):
        """Create a mask with rounded corners"""
        width, height = size
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)

        # Draw rounded rectangle
        draw.rounded_rectangle([(0, 0), (width, height)], radius=radius, fill=255)

        return np.array(mask) / 255.0  # Convert to 0.0-1.0 range

    # Create base rounded corner mask
    corner_radius = 15  # Adjust this value for more/less rounding
    rounded_mask_base = create_rounded_mask((cover_clip.w, cover_clip.h), corner_radius)

    # Create a mask that fades and has rounded corners
    def make_frame_mask(t):
        if t < cover_duration - fade_duration:
            # Fully opaque for first 2 seconds
            opacity = 1.0
        else:

            progress = (t - (cover_duration - fade_duration)) / fade_duration
            opacity = 1.0 - progress  # goes from 1.0 to 0.0

        # Apply both rounded corners and fade
        return rounded_mask_base * opacity

    # Create the mask clip
    mask_clip = VideoClip(is_mask=True)
    mask_clip.get_frame = make_frame_mask
    mask_clip.duration = cover_duration
    mask_clip.size = (cover_clip.w, cover_clip.h)

    # Apply the mask to the cover
    cover_clip = cover_clip.with_mask(mask_clip)

    final_clip = CompositeVideoClip(
        [video_clip, *text_clips, cover_clip], size=video_clip.size
    ).with_audio(audio_clip)

    final_clip.write_videofile(
        output_path,
        fps=target_fps,
        codec="libx264",
        audio_codec="aac",
        audio_bitrate="128k",
        ffmpeg_params=[
            "-pix_fmt",
            "yuv420p",
            "-profile:v",
            "baseline",
            "-level",
            "3.0",
            "-movflags",
            "+faststart",
        ],
    )


# def generate_reel(
#     audio_with_timestamps: AudioWithTimestamps,
#     video_path: str,
#     audio_path: str,
#     output_path: str,
#     target_fps: int = 30,
#     font_path: str = FONT_BANGERS_REGULAR,
# ):
#     video_clip = VideoFileClip(video_path)
#     audio_clip = AudioFileClip(audio_path)

#     words: list[CaptionWord] = audio_with_timestamps.words()

#     text_clips = []
#     for word in words:
#         txt_clip = (
#             TextClip(
#                 text=word.text,
#                 font_size=50,
#                 color="white",
#                 font=font_path,
#                 method="caption",
#                 size=(int(video_clip.w * 0.9), int(video_clip.h * 0.3)),
#                 stroke_color="black",
#                 stroke_width=2,
#             )
#             .with_position(("center", "center"))
#             .with_start(word.start)
#             .with_duration(word.end - word.start)
#         )
#         text_clips.append(txt_clip)

#     final_clip = CompositeVideoClip(
#         [video_clip, *text_clips], size=video_clip.size
#     ).with_audio(audio_clip)

#     final_clip.write_videofile(
#         output_path,
#         fps=target_fps,
#         codec="libx264",
#         audio_codec="aac",
#         audio_bitrate="128k",
#         ffmpeg_params=[
#             "-pix_fmt",
#             "yuv420p",
#             "-profile:v",
#             "baseline",
#             "-level",
#             "3.0",
#             "-movflags",
#             "+faststart",
#         ],
#     )


def save_random_segment(output_path: str, desired_length: int, padding_time: int = 5):
    """
    Extract a random segment from video with padding.

    Args:
        input_path: Path to input video file
        output_path: Path to save output video file
        desired_length: Desired length of output video in seconds
        padding_time: Padding time in seconds to add before/after random position (default: 5)

    The function picks a random position in the video, then extracts:
    [random_position - padding_time] to [random_position + (desired_length - padding_time)]

    This ensures the random position is within the output, with padding_time before it.
    """
    input_path = get_random_video_path()
    output_path = Path(output_path)

    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(
        f"Processing: {input_path.name}. Desired output length: {desired_length}s. Padding time: {padding_time}s"
    )

    try:
        # Load video
        video = VideoFileClip(str(input_path))
        total_duration = video.duration

        logger.info(
            f"Input video duration: {total_duration:.2f}s ({total_duration/60:.2f} minutes)"
        )

        # Check if video is long enough
        if total_duration < desired_length:
            logger.warning(
                f"Warning: Video ({total_duration:.2f}s) is shorter than desired length ({desired_length}s)"
            )
            start_time = 0
            end_time = total_duration
            actual_length = total_duration
            random_position = None
        else:
            # Calculate valid range for random position
            # Random position must allow for padding_time before it and remaining time after
            earliest_position = padding_time
            latest_position = total_duration - (desired_length - padding_time)

            if earliest_position >= latest_position:
                # Not enough room for padding, just extract from start
                logger.info(f"Warning: Not enough room for full padding")
                start_time = 0
                end_time = min(desired_length, total_duration)
                random_position = None
            else:
                # Pick random position and calculate segment
                random_position = random.uniform(earliest_position, latest_position)
                start_time = random_position - padding_time
                end_time = start_time + desired_length

                # Ensure we don't exceed video duration
                if end_time > total_duration:
                    end_time = total_duration
                    start_time = max(0, end_time - desired_length)

            actual_length = end_time - start_time
            if random_position:
                logger.info(f"Random position: {random_position:.2f}s")
            logger.info(
                f"Extracting: {start_time:.2f}s to {end_time:.2f}s (length: {actual_length:.2f}s)"
            )

        # Extract segment
        segment = video.subclipped(start_time, end_time)

        # Get crop dimensions for 9:16 mobile format
        width, height = segment.size
        x1, y1, x2, y2 = get_crop_dimensions(width, height)

        # Crop video to mobile format
        crop_effect = Crop(x1=x1, y1=y1, x2=x2, y2=y2)

        # Apply it using with_effects
        cropped_segment = segment.with_effects([crop_effect])
        logger.info(f"Saving to: {output_path}")

        # Write to file
        cropped_segment.write_videofile(
            str(output_path),
            codec="libx264",
            audio=False,
            preset="medium",
            logger=None,  # Suppress detailed progress
        )

        # Clean up
        cropped_segment.close()
        segment.close()
        video.close()

        logger.info(
            f"Completed: {output_path.name}. Output duration: {actual_length:.2f}s"
        )

        return True

    except Exception as e:
        logger.exception(f"Error processing video: {str(e)}")
        import traceback

        traceback.print_exc()
        return False
