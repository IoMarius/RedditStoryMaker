import base64
import random
from typing import Iterator
from .consts import AVAILABLE_VOICE_IDS


def _get_random_voice() -> str:
    return random.choice(AVAILABLE_VOICE_IDS)


def _audio_base64_to_bytes_iterator(
    base64_str: str, chunk_size: int = 32 * 1024
) -> Iterator[bytes]:
    audio_bytes = base64.b64decode(base64_str)
    for i in range(0, len(audio_bytes), chunk_size):
        yield audio_bytes[i : i + chunk_size]
