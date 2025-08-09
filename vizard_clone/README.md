# vizard_clone

A lightweight proof-of-concept for an automated vertical video generator
inspired by the *Vizard* application.  The repository only implements a
very small subset of the proposed feature set but keeps the public API
stable so additional functionality can be built on top of it.

## Usage

```bash
pip install -r requirements.txt
python -m vizard_clone.cli process input.mp4
```

The command above will produce a short clip in the ``processed``
directory.  The actual video analysis, subtitle generation and upload
steps are intentionally stubbed out in order to keep the example compact.

## Development

The repository contains unit tests for two core utilities: scene scoring
and ffmpeg muxing fallbacks.  Run them with ``pytest``.

## Legal

Only process and upload content you have the rights to use.
