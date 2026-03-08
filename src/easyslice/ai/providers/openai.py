from __future__ import annotations

import json
from dataclasses import dataclass

import requests

from easyslice.ai.base import SegmentRequest, StorySegmenter
from easyslice.domain.exceptions import AiResponseSchemaError
from easyslice.domain.models import Story, parse_stories


@dataclass(frozen=True)
class OpenAIConfig:
    api_key: str
    model: str = "gpt-4.1-mini"
    timeout_s: float = 120.0


class OpenAIStorySegmenter(StorySegmenter):
    def __init__(self, config: OpenAIConfig):
        self._config = config

    def segment(self, request: SegmentRequest) -> list[Story]:
        # Use Chat Completions with JSON-only response formatting.
        # The returned JSON is still validated against the exact Story schema.
        url = "https://api.openai.com/v1/chat/completions"

        user_prompt = (
            "Analyze this actual transcript and create viral-worthy story segments "
            "following the patterns you learned.\n\n"
            f"Transcript ({request.transcript_word_count} words):\n"
            f"{request.transcript_text}\n\n"
            "Return ONLY the JSON array following the exact structure from training.\n"
        )

        payload = {
            "model": self._config.model,
            "messages": [
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "response_format": {"type": "json_object"},
        }

        resp = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {self._config.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=self._config.timeout_s,
        )
        resp.raise_for_status()

        content = resp.json()["choices"][0]["message"]["content"]
        # We request json_object; content should be a JSON object.
        # We allow either {"stories": [...]} or raw list for flexibility, but enforce final schema.
        try:
            raw = json.loads(content)
        except Exception as e:  # pragma: no cover
            raise AiResponseSchemaError(f"OpenAI returned non-JSON: {e}") from e

        if isinstance(raw, dict) and "stories" in raw:
            raw = raw["stories"]

        try:
            return parse_stories(raw)
        except Exception as e:
            raise AiResponseSchemaError(f"OpenAI JSON did not match schema: {e}") from e
