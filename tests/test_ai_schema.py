import json
from pathlib import Path

from easyslice.domain.models import Story, parse_stories, stories_to_jsonable


def test_training_output_schema_parses_and_roundtrips() -> None:
    root = Path(__file__).resolve().parents[1]
    samples = [
        root / "in" / "training_data" / "output.json",
        root / "in" / "training_data" / "output2.json",
    ]

    for sample_path in samples:
        raw = json.loads(sample_path.read_text())
        stories = parse_stories(raw)
        assert isinstance(stories, list)
        assert all(isinstance(s, Story) for s in stories)

        dumped = stories_to_jsonable(stories)
        # Must keep exact keys present
        assert json.loads(json.dumps(dumped)) == dumped
        for story in dumped:
            assert set(story.keys()) == {"story_id", "story_title", "story_word_count", "clips"}
            for clip in story["clips"]:
                assert set(clip.keys()) == {"clip_id", "clip", "clip_word_count"}
