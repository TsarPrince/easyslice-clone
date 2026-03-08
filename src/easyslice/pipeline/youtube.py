from __future__ import annotations

import glob
import os
import subprocess
from pathlib import Path

from easyslice.domain.exceptions import ExternalToolError


def _filter_download_artifacts(paths: list[str]) -> list[str]:
    return [
        p
        for p in paths
        if os.path.isfile(p)
        and os.path.getsize(p) > 0
        and not p.endswith((
            ".part",
            ".ytdl",
            ".tmp",
            ".info.json",
            ".description",
        ))
    ]


def find_existing_video_path(temp_folder: Path, video_id: str) -> Path | None:
    preferred_exts = [".mp4", ".mkv", ".webm", ".mov"]

    candidates: list[str] = []
    for ext in preferred_exts:
        candidates.extend(glob.glob(str(temp_folder / f"{video_id}{ext}")))

    if not candidates:
        candidates = glob.glob(str(temp_folder / f"{video_id}.*"))

    candidates = _filter_download_artifacts(candidates)
    if not candidates:
        return None

    def sort_key(p: str) -> tuple[int, str]:
        lp = p.lower()
        if lp.endswith(".mp4"):
            rank = 0
        elif any(lp.endswith(ext) for ext in preferred_exts):
            rank = 1
        else:
            rank = 2
        return (rank, lp)

    return Path(sorted(set(candidates), key=sort_key)[0])


def download_video(url: str, temp_folder: Path, video_id: str) -> Path:
    cmd = [
        "yt-dlp",
        "--format",
        "best[height<=720][ext=mp4]/best[ext=mp4]/best",
        "--output",
        str(temp_folder / "%(id)s.%(ext)s"),
        "--no-playlist",
        url,
    ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
    except Exception as e:  # pragma: no cover
        raise ExternalToolError(f"yt-dlp failed: {e}") from e

    downloaded_files = glob.glob(str(temp_folder / f"{video_id}.*"))
    downloaded_files = _filter_download_artifacts(downloaded_files)
    if not downloaded_files:
        raise ExternalToolError("No downloaded file found")

    return Path(sorted(downloaded_files)[0])


def get_video(url: str, temp_folder: Path, video_id: str) -> Path:
    temp_folder.mkdir(parents=True, exist_ok=True)

    existing = find_existing_video_path(temp_folder, video_id)
    if existing:
        return existing
    return download_video(url, temp_folder, video_id)
