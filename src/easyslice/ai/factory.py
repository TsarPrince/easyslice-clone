from __future__ import annotations

from easyslice.ai.base import StorySegmenter
from easyslice.ai.providers.gemini import GeminiConfig, GeminiStorySegmenter
from easyslice.ai.providers.openai import OpenAIConfig, OpenAIStorySegmenter
from easyslice.config import Settings


def create_story_segmenter(settings: Settings) -> StorySegmenter:
    if settings.ai_provider == "gemini":
        if not settings.gemini_api_key:
            raise ValueError("Missing Gemini API key. Set gemini_api_key in config.json or EASYSLICE_GEMINI_API_KEY.")
        return GeminiStorySegmenter(GeminiConfig(api_key=settings.gemini_api_key, model=settings.gemini_model))

    if settings.ai_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("Missing OpenAI API key. Set openai_api_key in config.json or EASYSLICE_OPENAI_API_KEY.")
        return OpenAIStorySegmenter(OpenAIConfig(api_key=settings.openai_api_key, model=settings.openai_model))

    raise ValueError(f"Unknown ai_provider: {settings.ai_provider}")
