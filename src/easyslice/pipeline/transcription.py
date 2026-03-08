from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from easyslice.domain.exceptions import ExternalToolError
from easyslice.domain.models import Transcript


def convert_video_to_audio(video_path: Path, temp_folder: Path) -> Path:
    base_name = video_path.stem
    audio_path = temp_folder / f"{base_name}_full_audio.wav"

    cmd = [
        "ffmpeg",
        "-i",
        str(video_path),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        "-y",
        str(audio_path),
    ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
    except Exception as e:  # pragma: no cover
        raise ExternalToolError(f"ffmpeg audio conversion failed: {e}") from e

    return audio_path


def transcribe_word_timestamps(audio_path: Path) -> Transcript:
    try:
        import whisper  # type: ignore
    except Exception as e:  # pragma: no cover
        raise ImportError(
            "Whisper is not installed. Install with `pip install -e .[media]` "
            "or `pip install openai-whisper`."
        ) from e

    model = whisper.load_model("base")
    result = model.transcribe(str(audio_path), word_timestamps=True)

    all_words = []
    word_index = 0
    for segment in result["segments"]:
        for word_info in segment["words"]:
            all_words.append(
                {
                    "index": word_index,
                    "word": word_info["word"].strip(),
                    "start": word_info["start"],
                    "end": word_info["end"],
                }
            )
            word_index += 1

    payload = {"language": result["language"], "words": all_words}
    return Transcript.model_validate(payload)


def load_or_create_transcript(video_path: Path, transcript_path: Path, temp_folder: Path) -> Transcript:
    if transcript_path.exists():
        return Transcript.model_validate_json(transcript_path.read_text())

    temp_folder.mkdir(parents=True, exist_ok=True)
    audio_path = convert_video_to_audio(video_path, temp_folder)
    transcript = transcribe_word_timestamps(audio_path)

    transcript_path.write_text(json.dumps(transcript.model_dump(mode="json"), indent=2))
    return transcript
