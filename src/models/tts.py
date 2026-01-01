from dataclasses import dataclass
from typing import Iterator, List


@dataclass(frozen=True)
class CaptionWord:
    text: str
    start: float
    end: float


@dataclass(frozen=True)
class AudioWithTimestamps:
    audio: Iterator[bytes]
    characters: List[str]
    start_times: List[float]
    end_times: List[float]

    def words(self) -> List[CaptionWord]:
        """
        Convert character-level timestamps to word-level timestamps.
        """
        words: List[CaptionWord] = []
        buffer: List[str] = []
        word_start: float | None = None

        for ch, s, e in zip(self.characters, self.start_times, self.end_times):
            if ch.isspace():
                if buffer:
                    words.append(CaptionWord("".join(buffer), word_start, prev_end))
                    buffer = []
                    word_start = None
                continue

            if not buffer:
                word_start = s

            buffer.append(ch)
            prev_end = e

        if buffer:
            words.append(CaptionWord("".join(buffer), word_start, prev_end))

        return words
