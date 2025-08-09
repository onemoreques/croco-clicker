"""Subtitle and dubbing helpers (stub).

A production ready implementation would wrap Whisper for ASR, translation
and TTS for dubbing.  These operations are far beyond the scope of the
exercise so the functions below only provide minimal placeholders that
mimic the expected interfaces.  They are intentionally simplistic but
allow other modules to be imported without pulling large dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class SubtitleSegment:
    start: float
    end: float
    text: str


def transcribe_segment(src: str | Path, start_s: float, dur_s: float, tmp_dir: str, model: str):
    """Return a dummy transcription object.

    The stub pretends everything is English and simply returns a single
    subtitle covering the requested duration.
    """

    seg = SubtitleSegment(start_s, start_s + dur_s, "stub")
    return {"language": "en", "segments": [seg]}


def write_srt(segments: List[SubtitleSegment], path: str | Path) -> Path:
    path = Path(path)
    with path.open("w", encoding="utf-8") as fh:
        for idx, seg in enumerate(segments, 1):
            fh.write(f"{idx}\n")
            fh.write(f"00:00:00,000 --> 00:00:00,000\n{seg.text}\n\n")
    return path


def burn_subtitles(video: str | Path, srt: str | Path, out_path: str | Path) -> Path:
    """Placeholder that simply copies the source video to ``out_path``."""
    src = Path(video)
    out = Path(out_path)
    out.write_bytes(src.read_bytes())
    return out
