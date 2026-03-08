from __future__ import annotations

import json
from dataclasses import dataclass

import requests

from easyslice.ai.base import SegmentRequest, StorySegmenter
from easyslice.domain.exceptions import AiResponseSchemaError
from easyslice.domain.models import Story, parse_stories


@dataclass(frozen=True)
class GeminiConfig:
    api_key: str
    model: str = "gemini-2.5-flash"
    timeout_s: float = 120.0


class GeminiStorySegmenter(StorySegmenter):
    def __init__(self, config: GeminiConfig):
        self._config = config

    def segment(self, request: SegmentRequest) -> list[Story]:
        api_url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self._config.model}:generateContent?key={self._config.api_key}"
        )

        current_prompt = (
            "Analyze this actual transcript and create viral-worthy story segments "
            "following the patterns you learned.\n\n"
            f"Transcript ({request.transcript_word_count} words):\n"
            f"{request.transcript_text}\n\n"
            "Return ONLY the JSON array following the exact structure from training.\n"
        )

        payload = {
            "contents": [{"parts": [{"text": request.system_prompt + current_prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"},
        }

        response = requests.post(
            api_url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=self._config.timeout_s,
        )
        response.raise_for_status()

        json_text = (
            response.json()
            .get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "[]")
        )

        if isinstance(json_text, str) and json_text.strip().startswith("```json"):
            json_text = json_text.strip()[7:-3].strip()

        try:
            raw = json.loads(json_text)
        except Exception as e:  # pragma: no cover
            raise AiResponseSchemaError(f"Gemini returned non-JSON: {e}") from e

        try:
            return parse_stories(raw)
        except Exception as e:
            raise AiResponseSchemaError(f"Gemini JSON did not match schema: {e}") from e
