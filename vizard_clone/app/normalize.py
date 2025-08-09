"""Video normalisation helpers.

The function implemented here performs the bare minimum required for the
unit tests.  It strips audio and ensures the video stream is constant
frame rate 30fps H.264.  Error handling is intentionally forgiving –
ffmpeg's ``-err_detect ignore_err`` option is used to attempt decoding of
slightly broken input files.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from .ffmpeg_utils import find_ffmpeg, _run


def normalize_video_only(src: str | Path, out_path: str | Path) -> Path:
    """Normalise *src* to a clean video-only H.264 file.

    Parameters
    ----------
    src: path to the input video.
    out_path: destination for the normalised video.
    """

    ffmpeg = find_ffmpeg()
    src = Path(src)
    out_path = Path(out_path)

    cmd = [
        ffmpeg,
        "-y",
        "-err_detect",
        "ignore_err",
        "-analyzeduration",
        "0",
        "-probesize",
        "2M",
        "-i",
        str(src),
        "-map",
        "0:v:0",
        "-an",
        "-vf",
        "fps=30",
        "-r",
        "30",
        "-pix_fmt",
        "yuv420p",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-movflags",
        "+faststart",
        "-vsync",
        "cfr",
        str(out_path),
    ]
    _run(cmd)
    return out_path
