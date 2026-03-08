from __future__ import annotations

import json
from pathlib import Path

from easyslice.ai.base import SegmentRequest, StorySegmenter
from easyslice.domain.models import Story, Transcript, parse_stories, stories_to_jsonable, transcript_to_text
from easyslice.pipeline.prompts import build_system_prompt


def load_or_create_stories(
    *,
    segmenter: StorySegmenter,
    transcript: Transcript,
    stories_path: Path,
    training_folder: Path,
) -> list[Story]:
    if stories_path.exists():
        raw = json.loads(stories_path.read_text())
        return parse_stories(raw)

    system_prompt = build_system_prompt(training_folder)
    transcript_text = transcript_to_text(transcript)

    stories = segmenter.segment(
        SegmentRequest(
            transcript_text=transcript_text,
            transcript_word_count=len(transcript.words),
            system_prompt=system_prompt,
        )
    )

    stories_path.write_text(json.dumps(stories_to_jsonable(stories), indent=2))
    return stories
