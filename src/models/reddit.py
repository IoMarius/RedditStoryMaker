from dataclasses import dataclass
import re
from typing import Iterator
from warnings import deprecated


@dataclass
class Subreddit:
    name: str
    url: str


@dataclass
class Story:
    id: str
    hook: str
    content: str
    conclusion: str
    caption: str
    hashtags: str

    def to_string(self) -> str:
        return f"{self.hook}\n\n{self.content}\n\n{self.conclusion}"

    @deprecated("Do not use. Use captions with timestamps.")
    def to_captions(
        self, total_duration: int = 60, words_per_chunk: int = 5
    ) -> list[tuple[str, int]]:
        """
        Split story into phrases for captions.
        total_duration: total audio duration in seconds
        words_per_chunk: approximate number of words per caption line
        Returns: list of (text, duration_in_seconds)
        """

        text = f"{self.hook}. {self.content}. {self.conclusion}"

        words = re.findall(r"\S+", text)

        chunks = [
            " ".join(words[i : i + words_per_chunk])
            for i in range(0, len(words), words_per_chunk)
        ]

        chunk_duration = max(1, total_duration // len(chunks))

        return [(chunk, chunk_duration) for chunk in chunks]


@dataclass
class RawStory:
    id: str
    title: str
    body: str
    score: int


@dataclass
class StoredStory:
    story: RawStory


@dataclass
class PipelineResult:
    video_path: str
    caption: str
    hashtags: str
