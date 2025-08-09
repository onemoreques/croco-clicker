"""Rendering pipeline stubs.

The function :func:`render_window` represents a simplified end-to-end
process for a single clip.  It does not implement the sophisticated
features from the original project such as dynamic cropping and subtitle
burn-in; instead it merely demonstrates how the utilities can be wired
together.  This keeps the module lightweight for the unit tests while
providing a clear extension point for future work.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from . import config
from .ffmpeg_utils import mux_video_with_audio, pngs_to_mp4
from .focus_track import compute_focus_path
from .subs import burn_subtitles, transcribe_segment, write_srt


def render_window(
    source: str | Path,
    start_s: float,
    dur_s: float,
    tmp_dir: str | Path,
    out_path: str | Path,
) -> Path:
    """Render a very small proof-of-concept clip.

    The function performs the following minimal steps:

    * transcribe the segment (stub)
    * write a trivial SRT file
    * simply copy the video portion via ``ffmpeg`` and mux the audio using
      :func:`mux_video_with_audio`
    """

    tmp_dir = Path(tmp_dir)
    out_path = Path(out_path)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    srt_path = tmp_dir / "subs.srt"

    # Subtitle workflow (dummy)
    result = transcribe_segment(source, start_s, dur_s, str(tmp_dir), config.WHISPER_MODEL)
    segments = result["segments"]
    write_srt(segments, srt_path)

    # Extract video frames (as a placeholder we simply copy using ffmpeg)
    silent_video = tmp_dir / "silent.mp4"
    pngs_to_mp4(tmp_dir, 30, silent_video)  # this will fail if no PNGs; placeholder

    # Mux audio using helper which includes silence fallback
    mux_video_with_audio(silent_video, source, start_s, dur_s, out_path)

    # Burn subtitles (dummy copy)
    burn_subtitles(out_path, srt_path, out_path)
    return out_path
