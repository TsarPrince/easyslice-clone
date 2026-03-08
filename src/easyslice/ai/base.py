from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from easyslice.domain.models import Story


@dataclass(frozen=True)
class SegmentRequest:
    transcript_text: str
    transcript_word_count: int
    system_prompt: str


class StorySegmenter(Protocol):
    def segment(self, request: SegmentRequest) -> list[Story]:
        """Return stories following the exact training schema."""

        raise NotImplementedError
