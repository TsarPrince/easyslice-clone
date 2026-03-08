from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class StoryClip(BaseModel):
    """A single continuous excerpt chosen from the transcript (AI output schema)."""

    model_config = ConfigDict(extra="forbid")

    clip_id: int
    clip: str
    clip_word_count: int


class Story(BaseModel):
    """A standalone story made of 1+ clips (AI output schema)."""

    model_config = ConfigDict(extra="forbid")

    story_id: int
    story_title: str
    story_word_count: int
    clips: list[StoryClip]


class TranscriptWord(BaseModel):
    """Whisper word-level transcript token."""

    model_config = ConfigDict(extra="forbid")

    index: int
    word: str
    start: float
    end: float


class Transcript(BaseModel):
    model_config = ConfigDict(extra="forbid")

    language: str
    words: list[TranscriptWord]


class ProcessedClip(BaseModel):
    """A clip mapped back onto transcript indices + timestamps."""

    model_config = ConfigDict(extra="forbid")

    start_index: int
    end_index: int
    word_count: int
    start_time: float
    end_time: float
    duration: float
    clip: str


class ProcessedStory(BaseModel):
    model_config = ConfigDict(extra="forbid")

    story_title: str
    total_duration: float
    total_word_count: int
    clips: list[ProcessedClip]


def parse_stories(raw: Any) -> list[Story]:
    """Parse and validate the exact AI output schema."""

    if raw is None:
        return []
    # pydantic handles list parsing via TypeAdapter, but keep dependency surface small.
    return [Story.model_validate(item) for item in raw]


def stories_to_jsonable(stories: list[Story]) -> list[dict[str, Any]]:
    return [s.model_dump(mode="json") for s in stories]


def transcript_to_text(transcript: Transcript) -> str:
    return " ".join(w.word for w in transcript.words)
