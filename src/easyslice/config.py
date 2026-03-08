from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

AiProviderName = Literal["gemini", "openai"]


@dataclass(frozen=True)
class Settings:
    ai_provider: AiProviderName = "gemini"

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"

    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"

    # Paths
    output_root: Path = Path("out")
    temp_root: Path = Path("temp")
    training_folder: Path = Path("in/training_data")


def load_settings(config_path: Path | str = "config.json") -> Settings:
    """Load settings from env + config.json (if present).

    Env vars (override file):
    - EASYSLICE_AI_PROVIDER: gemini|openai
    - EASYSLICE_GEMINI_API_KEY
    - EASYSLICE_GEMINI_MODEL
    - EASYSLICE_OPENAI_API_KEY
    - EASYSLICE_OPENAI_MODEL
    - EASYSLICE_OUTPUT_ROOT
    - EASYSLICE_TEMP_ROOT
    - EASYSLICE_TRAINING_FOLDER
    """

    config_file_data: dict[str, object] = {}
    config_path = Path(config_path)
    if config_path.exists():
        config_file_data = json.loads(config_path.read_text())

    ai_provider = (os.getenv("EASYSLICE_AI_PROVIDER") or str(config_file_data.get("ai_provider", "gemini"))).strip()
    if ai_provider not in ("gemini", "openai"):
        raise ValueError(f"Unsupported ai_provider: {ai_provider}")

    gemini_api_key = os.getenv("EASYSLICE_GEMINI_API_KEY") or config_file_data.get("gemini_api_key")
    gemini_api_key = str(gemini_api_key) if gemini_api_key else None

    gemini_model = (os.getenv("EASYSLICE_GEMINI_MODEL") or str(config_file_data.get("gemini_model", "gemini-2.5-flash"))).strip()

    openai_api_key = os.getenv("EASYSLICE_OPENAI_API_KEY") or config_file_data.get("openai_api_key")
    openai_api_key = str(openai_api_key) if openai_api_key else None
    openai_model = (os.getenv("EASYSLICE_OPENAI_MODEL") or str(config_file_data.get("openai_model", "gpt-4.1-mini"))).strip()

    output_root = Path(os.getenv("EASYSLICE_OUTPUT_ROOT") or str(config_file_data.get("output_root", "out")))
    temp_root = Path(os.getenv("EASYSLICE_TEMP_ROOT") or str(config_file_data.get("temp_root", "temp")))
    training_folder = Path(os.getenv("EASYSLICE_TRAINING_FOLDER") or str(config_file_data.get("training_folder", "in/training_data")))

    return Settings(
        ai_provider=ai_provider,  # type: ignore[arg-type]
        gemini_api_key=gemini_api_key,
        gemini_model=gemini_model,
        openai_api_key=openai_api_key,
        openai_model=openai_model,
        output_root=output_root,
        temp_root=temp_root,
        training_folder=training_folder,
    )
