from __future__ import annotations

import re
from difflib import SequenceMatcher

from easyslice.domain.models import ProcessedClip, ProcessedStory, Story, Transcript


def _normalize_word(w: str) -> str:
    return re.sub(r"[^\w]", "", w.lower())


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def _window_similarity(a_words: list[str], b_words: list[str]) -> float:
    return _similarity(" ".join(a_words), " ".join(b_words))


def map_stories_to_transcript(
    *,
    stories: list[Story],
    transcript: Transcript,
    fuzzy_match_length: int = 8,
    sim_threshold: float = 0.6,
) -> list[ProcessedStory]:
    transcript_words_raw = [w.word for w in transcript.words]
    transcript_words = [_normalize_word(w) for w in transcript_words_raw]

    processed_stories: list[ProcessedStory] = []

    for story in stories:
        story_clips: list[ProcessedClip] = []
        skip_story = False

        for clip_obj in story.clips:
            clip_words_raw = clip_obj.clip.split()
            clip_words = [_normalize_word(w) for w in clip_words_raw]

            clip_length = len(clip_words)
            anchor = min(fuzzy_match_length, clip_length)

            start_anchor = clip_words[:anchor]
            end_anchor = clip_words[-anchor:]

            best_start: int | None = None
            best_start_score = 0.0

            best_end: int | None = None
            best_end_score = 0.0

            for i in range(len(transcript_words) - anchor):
                window = transcript_words[i : i + anchor]
                score = _window_similarity(start_anchor, window)
                if score > best_start_score:
                    best_start_score = score
                    best_start = i

            for i in range(len(transcript_words) - anchor):
                window = transcript_words[i : i + anchor]
                score = _window_similarity(end_anchor, window)
                if score > best_end_score:
                    best_end_score = score
                    best_end = i + anchor - 1

            if (
                best_start is None
                or best_end is None
                or best_start_score < sim_threshold
                or best_end_score < sim_threshold
                or best_end <= best_start
            ):
                skip_story = True
                break

            start_index = best_start
            end_index = best_end

            start_time = float(transcript.words[start_index].start)
            end_time = float(transcript.words[end_index].end)

            story_clips.append(
                ProcessedClip(
                    start_index=start_index,
                    end_index=end_index,
                    word_count=end_index - start_index + 1,
                    start_time=start_time,
                    end_time=end_time,
                    duration=float(end_time - start_time),
                    clip=" ".join(transcript_words_raw[start_index : end_index + 1]),
                )
            )

        if not skip_story:
            processed_stories.append(
                ProcessedStory(
                    story_title=story.story_title,
                    total_duration=sum(c.duration for c in story_clips),
                    total_word_count=sum(c.word_count for c in story_clips),
                    clips=story_clips,
                )
            )

    return processed_stories
