import base64
import os
from typing import Iterator
from elevenlabs import VoiceSettings
from core import logger
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from models.reddit import Story
from models.tts import AudioWithTimestamps
from .utils import _audio_base64_to_bytes_iterator, _get_random_voice


load_dotenv()


def convert_to_speech(story: Story) -> Iterator[bytes]:
    client = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
    )

    model_id = os.getenv("ELEVENLABS_MODEL")
    voice_id = _get_random_voice()

    logger.debug(
        f"Sending tts request to elevenlabs. Model {model_id} voice {voice_id}."
    )

    audio = client.text_to_speech.convert(
        text=story.to_string(),
        voice_id=voice_id,
        model_id=model_id,
        output_format="mp3_44100_128",
    )

    logger.debug("Received response from elevenlabs.")
    return audio


def convert_to_speech_timestamped(story: Story) -> AudioWithTimestamps:
    client = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
    )

    model_id = os.getenv("ELEVENLABS_MODEL")
    voice_id = _get_random_voice()

    logger.debug(
        f"Sending tts request to elevenlabs. Model {model_id} voice {voice_id}."
    )

    response = client.text_to_speech.convert_with_timestamps(
        text=story.to_string(),
        voice_id=voice_id,
        model_id=model_id,
        output_format="mp3_44100_128",
        voice_settings=VoiceSettings(speed=1.1, stability=0.8),
    )
    logger.debug("Received response from elevenlabs.")

    alignment = response.normalized_alignment or response.alignment

    return AudioWithTimestamps(
        audio=_audio_base64_to_bytes_iterator(response.audio_base_64),
        characters=alignment.characters,
        start_times=alignment.character_start_times_seconds,
        end_times=alignment.character_end_times_seconds,
    )
