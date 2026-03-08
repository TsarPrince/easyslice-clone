from __future__ import annotations

import argparse
from pathlib import Path

from easyslice.ai.factory import create_story_segmenter
from easyslice.config import load_settings
from easyslice.pipeline.captions import CAPTION_PRESETS, caption_all_stories
from easyslice.pipeline.clip_matching import map_stories_to_transcript
from easyslice.pipeline.story_segmentation import load_or_create_stories
from easyslice.pipeline.transcription import load_or_create_transcript
from easyslice.pipeline.utils import extract_video_id
from easyslice.pipeline.video_editing import create_vertical_clip
from easyslice.pipeline.youtube import get_video
from easyslice.ui.progress import Step, header, info
from easyslice.pipeline.utils import safe_filename


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="easyslice")
    p.add_argument("--config", default="config.json", help="Path to config.json")
    p.add_argument("--video-url", required=True, help="YouTube URL")
    p.add_argument(
        "--captions",
        action="store_true",
        help="Also generate captioned videos (MoviePy/PIL). Requires media deps.",
    )
    p.add_argument(
        "--caption-presets",
        default=",".join(CAPTION_PRESETS.keys()),
        help=f"Comma-separated caption presets. Available: {', '.join(CAPTION_PRESETS.keys())}",
    )
    p.add_argument(
        "--caption-workers",
        type=int,
        default=None,
        help="Max worker threads for caption generation (default: MoviePy/OS decides).",
    )
    return p


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)

    header("easyslice")
    with Step(label="Loading configuration"):
        settings = load_settings(args.config)
    with Step(label=f"Initializing AI provider ({settings.ai_provider})"):
        segmenter = create_story_segmenter(settings)

    video_id = extract_video_id(args.video_url)
    output_folder = settings.output_root / video_id
    temp_folder = settings.temp_root / video_id
    output_folder.mkdir(parents=True, exist_ok=True)
    temp_folder.mkdir(parents=True, exist_ok=True)

    info(f"video_id: {video_id}")
    info(f"output:  {output_folder}")

    with Step(label="Downloading video (yt-dlp)"):
        video_path = get_video(args.video_url, temp_folder, video_id)

    transcript_path = output_folder / f"{video_id}_transcript.json"
    with Step(label="Transcribing (whisper)"):
        transcript = load_or_create_transcript(video_path, transcript_path, temp_folder)

    stories_path = output_folder / f"{video_id}_stories.json"
    with Step(label="Segmenting transcript (AI)"):
        stories = load_or_create_stories(
            segmenter=segmenter,
            transcript=transcript,
            stories_path=stories_path,
            training_folder=settings.training_folder,
        )

    with Step(label="Matching clips back to transcript"):
        processed_stories = map_stories_to_transcript(stories=stories, transcript=transcript)

    info(f"stories: {len(processed_stories)}")

    for i, story in enumerate(processed_stories, start=1):
        expected = output_folder / f"story_{i}_{safe_filename(story.story_title)}.mp4"
        if expected.exists() and expected.stat().st_size > 0:
            info(f"skip: {expected}")
            continue

        with Step(label=f"Rendering vertical clip {i}/{len(processed_stories)} (ffmpeg)"):
            create_vertical_clip(video_path=video_path, story=story, story_index=i, output_folder=output_folder)

    if args.captions:
        presets = [p.strip() for p in str(args.caption_presets).split(",") if p.strip()]
        unknown = [p for p in presets if p not in CAPTION_PRESETS]
        if unknown:
            raise SystemExit(
                f"Unknown caption preset(s): {', '.join(unknown)}. "
                f"Available: {', '.join(CAPTION_PRESETS.keys())}"
            )

        with Step(label=f"Rendering captions (moviepy) [{', '.join(presets)}]"):
            caption_all_stories(
                processed_stories=processed_stories,
                transcript=transcript,
                output_folder=output_folder,
                presets=presets,  # type: ignore[arg-type]
                max_workers=args.caption_workers,
            )


if __name__ == "__main__":
    main()
