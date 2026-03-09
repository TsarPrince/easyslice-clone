# easyslice

Productionized Python module version of `final.ipynb`.

## Quickstart

- Install base deps: `pip install -e .`
- Install full media deps: `pip install -e .[media]`

## Reproduce the exact .venv deps

This repo includes a pinned `requirements.txt` (runtime-focused; excludes Jupyter/IPython/pytest tooling):

- Install pinned deps: `./.venv/bin/python -m pip install -r requirements.txt`
- Install the project without changing deps: `./.venv/bin/python -m pip install -e . --no-deps`

## Config

Create `config.json` (see `config.json.sample`).

- Switch providers by changing `ai_provider` to `gemini` or `openai`.
- The output is validated against the same `Story` schema in both cases.

## Run

```bash
python -m easyslice --help
# or
 easyslice --help

# end-to-end (includes captioning)
easyslice --video-url 'https://www.youtube.com/watch?v=...' --captions

# choose caption styles
easyslice --video-url 'https://www.youtube.com/watch?v=...' --captions --caption-presets sentence_bg_highlight,single_word
```

## Sample Usage

```bash
easyslice --video-url 'https://www.youtube.com/watch?v=zB_OApdxcno'
```

<img width="2920" height="1636" alt="image" src="https://github.com/user-attachments/assets/bab0ffac-168c-4de4-b8c5-d6d7b8f1cf87" />


results: [@theoginfochips/shorts](https://www.youtube.com/@theoginfochips/shorts)
