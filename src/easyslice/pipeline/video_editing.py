from __future__ import annotations

import subprocess
from pathlib import Path

from easyslice.domain.exceptions import ExternalToolError
from easyslice.domain.models import ProcessedStory
from easyslice.pipeline.utils import safe_filename


def create_vertical_clip(*, video_path: Path, story: ProcessedStory, story_index: int, output_folder: Path) -> Path:
    output_folder.mkdir(parents=True, exist_ok=True)

    safe_title = safe_filename(story.story_title)
    output_file = output_folder / f"story_{story_index}_{safe_title}.mp4"

    # Idempotency: if the clip already exists and is non-empty, reuse it.
    if output_file.exists() and output_file.stat().st_size > 0:
        return output_file

    filter_parts: list[str] = []
    input_parts: list[str] = ["-i", str(video_path)]

    for i, clip in enumerate(story.clips):
        start_time = clip.start_time
        duration = clip.duration

        filter_parts.append(f"[0:v]trim=start={start_time}:duration={duration},setpts=PTS-STARTPTS[v{i}]")
        filter_parts.append(f"[0:a]atrim=start={start_time}:duration={duration},asetpts=PTS-STARTPTS[a{i}]")

    video_inputs = "".join([f"[v{i}]" for i in range(len(story.clips))])
    audio_inputs = "".join([f"[a{i}]" for i in range(len(story.clips))])

    filter_parts.append(f"{video_inputs}concat=n={len(story.clips)}:v=1:a=0[vconcat]")
    filter_parts.append(f"{audio_inputs}concat=n={len(story.clips)}:v=0:a=1[aconcat]")

    filter_parts.append(
        "[vconcat]scale=1080:1920:force_original_aspect_ratio=decrease,"
        "pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1[vout]"
    )

    filter_complex = ";".join(filter_parts)

    cmd = ["ffmpeg", "-y"] + input_parts + [
        "-filter_complex",
        filter_complex,
        "-map",
        "[vout]",
        "-map",
        "[aconcat]",
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "23",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        str(output_file),
    ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:  # pragma: no cover
        raise ExternalToolError(f"FFmpeg failed: {e.stderr}") from e

    return output_file
