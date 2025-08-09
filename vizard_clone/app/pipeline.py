"""High level processing pipeline (stub)."""
from __future__ import annotations

from pathlib import Path
from typing import List

from . import config
from .render import render_window


def process_video(src_path: str | Path, out_dir: str | Path) -> List[Path]:
    """Process ``src_path`` and return a list of generated clips.

    The function is intentionally tiny; it simply renders a single
    5-second window starting at the beginning of the video.  This mirrors
    the interface of the full project while keeping the execution time
    minimal for the unit tests.
    """

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    clip_path = out_dir / "clip.mp4"
    render_window(src_path, 0, 5, out_dir / "tmp", clip_path)
    return [clip_path]
