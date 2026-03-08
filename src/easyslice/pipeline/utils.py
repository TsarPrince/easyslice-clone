from __future__ import annotations

import re


def extract_video_id(url: str) -> str:
    match = re.search(r"(?<=v=)[\w-]+", url)
    if match:
        return match.group(0)
    match = re.search(r"youtu\.be/([\w-]+)", url)
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract video ID from URL: {url}")


def safe_filename(name: str) -> str:
    return re.sub(r"[^\w\-_]", "_", name)
