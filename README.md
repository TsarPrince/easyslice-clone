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

<img width="2390" height="1644" alt="image" src="https://github.com/user-attachments/assets/5f78c790-23ca-45ac-966e-a206a3e26e7e" />



