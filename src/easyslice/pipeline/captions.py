from __future__ import annotations

import os
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from easyslice.domain.models import ProcessedStory, Transcript
from easyslice.pipeline.utils import safe_filename

CaptionPresetName = Literal["sentence_bg_highlight", "single_word"]


# RGBA tuples from the notebook
DARK_GREY = (0, 48, 73, 255)
YELLOW = (255, 189, 89, 255)
RED = (239, 35, 60, 255)
WHITE = (255, 255, 255, 255)


CAPTION_PRESETS: dict[str, dict[str, object]] = {
    "sentence_bg_highlight": {
        "name": "Sentence Background + Word Text",
        "description": "Highlighted sentence background with current word in different color",
        "font_size": 65,
        "bg_color": YELLOW,
        "text_color": DARK_GREY,
        "highlight_color": RED,
        "padding": 20,
        "border_radius": 15,
        "mode": "sentence_bg",
    },
    "single_word": {
        "name": "Single Word Display",
        "description": "One word at a time with rounded background",
        "font_size": 80,
        "bg_color": YELLOW,
        "text_color": DARK_GREY,
        "padding": 25,
        "border_radius": 20,
        "mode": "single_word",
    },
}


def _require_caption_deps():
    try:
        from moviepy import ImageClip, VideoFileClip, CompositeVideoClip  # noqa: F401
        from PIL import Image, ImageDraw, ImageFont  # noqa: F401
        import numpy as np  # noqa: F401
    except Exception as e:  # pragma: no cover
        raise ImportError(
            "Captioning deps not installed. Install with `pip install -e .[media]`."
        ) from e


def draw_rounded_rectangle(draw, bbox, radius, fill):
    x1, y1, x2, y2 = bbox
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)

    draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill)
    draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill)


def create_sentence_image_with_highlight(sentence_words, highlight_idx, style, video_width=1080):
    _require_caption_deps()
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np

    font_size = style["font_size"]
    bg_color = style["bg_color"]
    text_color = style["text_color"]
    padding = style["padding"]
    border_radius = style["border_radius"]
    mode = style["mode"]

    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(font_size))

    words_text = [word["word"] for word in sentence_words]

    if mode == "single_word":
        current_word = words_text[highlight_idx]
        temp_img = Image.new("RGBA", (1000, 200), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_img)

        word_bbox = temp_draw.textbbox((0, 0), current_word, font=font)
        word_width = word_bbox[2] - word_bbox[0]
        word_height = word_bbox[3] - word_bbox[1]

        img_width = word_width + (padding * 2)
        img_height = word_height + (padding * 2)

        img = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        draw_rounded_rectangle(draw, (0, 0, img_width, img_height), int(border_radius), bg_color)

        text_x = (img_width - word_width) // 2
        text_y = (img_height - word_height) // 2
        draw.text((text_x, text_y), current_word, font=font, fill=text_color)

        return np.array(img)

    temp_img = Image.new("RGBA", (2000, 200), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)

    word_positions = []
    current_x = 0

    for i, word in enumerate(words_text):
        word_bbox = temp_draw.textbbox((current_x, 0), word, font=font)
        word_width = word_bbox[2] - word_bbox[0]
        word_height = word_bbox[3] - word_bbox[1]

        word_positions.append(
            {
                "word": word,
                "x": current_x,
                "width": word_width,
                "height": word_height,
                "highlighted": i == highlight_idx,
            }
        )

        current_x += word_width
        if i < len(words_text) - 1:
            space_width = temp_draw.textbbox((0, 0), " ", font=font)[2]
            current_x += space_width

    total_text_width = current_x
    text_height = max(pos["height"] for pos in word_positions)

    img_width = min(total_text_width + (padding * 2), video_width - 40)
    img_height = text_height + (padding * 2)

    img = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw_rounded_rectangle(draw, (0, 0, img_width, img_height), int(border_radius), bg_color)

    start_x = (img_width - total_text_width) // 2
    text_y = padding

    current_x = start_x
    for word_info in word_positions:
        word = word_info["word"]

        color = style["highlight_color"] if word_info["highlighted"] else text_color
        outline_color = color

        for adj in range(-1, 2):
            for adj2 in range(-1, 2):
                if adj != 0 or adj2 != 0:
                    draw.text((current_x + adj, text_y + adj2), word, font=font, fill=outline_color)

        draw.text((current_x, text_y), word, font=font, fill=color)

        current_x += word_info["width"]
        if word_info is not word_positions[-1]:
            space_width = draw.textbbox((0, 0), " ", font=font)[2]
            current_x += space_width

    return np.array(img)


def create_moviepy_advanced_captions(
    *,
    story: ProcessedStory,
    transcript: Transcript,
    input_video_path: Path,
    output_folder: Path,
    preset_name: CaptionPresetName,
    story_index: int,
) -> Path:
    _require_caption_deps()
    from moviepy import ImageClip, VideoFileClip, CompositeVideoClip

    style = CAPTION_PRESETS[preset_name]

    video = VideoFileClip(str(input_video_path))
    video_duration = video.duration

    all_caption_words = []
    story_start_time = story.clips[0].start_time

    for clip in story.clips:
        clip_words = transcript.words[clip.start_index : clip.end_index + 1]
        for word_data in clip_words:
            word_time_in_story = word_data.start - story_start_time
            if word_time_in_story < 0:
                word_time_in_story = 0

            clean_word = word_data.word.strip()
            if clean_word:
                all_caption_words.append(
                    {
                        "word": clean_word,
                        "start_time": word_time_in_story,
                        "duration": min(word_data.end - word_data.start, 1.5),
                    }
                )

    if not all_caption_words:
        video.close()
        return input_video_path

    caption_clips = []

    if style["mode"] == "single_word":
        for word_info in all_caption_words:
            word_img_array = create_sentence_image_with_highlight(
                [word_info],
                0,
                style,
                video_width=int(video.w),
            )

            word_clip = ImageClip(word_img_array, duration=word_info["duration"])
            word_clip = word_clip.with_start(word_info["start_time"])
            word_clip = word_clip.with_position(("center", 0.85), relative=True)
            caption_clips.append(word_clip)

            if word_info["start_time"] + word_info["duration"] > video_duration:
                break

    else:
        sentences = []
        current_sentence = []
        for word_info in all_caption_words:
            current_sentence.append(word_info)
            if len(current_sentence) >= 3 or word_info == all_caption_words[-1]:
                if current_sentence:
                    sentences.append(current_sentence.copy())
                    current_sentence = []

        for sentence_words in sentences:
            for word_idx, word_info in enumerate(sentence_words):
                sentence_img_array = create_sentence_image_with_highlight(
                    sentence_words,
                    word_idx,
                    style,
                    video_width=int(video.w),
                )

                word_clip = ImageClip(sentence_img_array, duration=word_info["duration"])
                word_clip = word_clip.with_start(word_info["start_time"])
                word_clip = word_clip.with_position(("center", 0.85), relative=True)
                caption_clips.append(word_clip)

                if word_info["start_time"] + word_info["duration"] > video_duration:
                    break

    final_video = CompositeVideoClip([video] + caption_clips)

    output_folder.mkdir(parents=True, exist_ok=True)
    safe_title = safe_filename(story.story_title)
    output_file = output_folder / f"{preset_name}_story_{story_index}_{safe_title}.mp4"

    final_video.write_videofile(str(output_file), codec="libx264", audio_codec="aac")

    final_video.close()
    video.close()

    return output_file


def caption_all_stories(
    *,
    processed_stories: list[ProcessedStory],
    transcript: Transcript,
    output_folder: Path,
    presets: list[CaptionPresetName] | None = None,
    max_workers: int | None = None,
) -> list[Path]:
    if presets is None:
        presets = ["sentence_bg_highlight", "single_word"]

    moviepy_folder = output_folder / "moviepy_captions"

    def run_one(i_story):
        i, story = i_story
        preset = presets[i % len(presets)]
        safe_title = safe_filename(story.story_title)
        story_index = i + 1
        expected_out = moviepy_folder / f"{preset}_story_{story_index}_{safe_title}.mp4"

        if expected_out.exists() and expected_out.stat().st_size > 0:
            return expected_out

        original_clip_path = output_folder / f"story_{story_index}_{safe_title}.mp4"
        if not original_clip_path.exists():
            return None

        try:
            return create_moviepy_advanced_captions(
                story=story,
                transcript=transcript,
                input_video_path=original_clip_path,
                output_folder=moviepy_folder,
                preset_name=preset,
                story_index=story_index,
            )
        except Exception:
            return None

    if not processed_stories:
        return []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(run_one, enumerate(processed_stories)))

    return [r for r in results if r is not None]
