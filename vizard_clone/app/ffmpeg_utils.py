"""Helpers around ffmpeg execution.

The real project makes extensive use of ffmpeg for video processing.  In
order to keep the tests lightweight we only implement a subset of the
behaviour that is required for the unit tests.  The implementation still
tries to closely follow the contract described in the project
specification so that the stubs can be expanded in the future.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from . import config


class FFMpegError(RuntimeError):
    """Raised when ffmpeg failed to produce the expected output."""


def find_ffmpeg() -> str:
    """Return path to the ffmpeg executable.

    The function checks ``config.FFMPEG_PATH`` first, then looks in
    ``PATH`` using :func:`shutil.which`.  Finally it falls back to the
    Windows default ``D:\\ffmpeg\\bin\\ffmpeg.exe``.  The return value is
    guaranteed to be a string; if the executable cannot be located a
    ``RuntimeError`` is raised.
    """

    if config.FFMPEG_PATH and Path(config.FFMPEG_PATH).exists():
        return str(config.FFMPEG_PATH)

    path = shutil.which("ffmpeg")
    if path:
        return path

    windows_path = r"D:\\ffmpeg\\bin\\ffmpeg.exe"
    if os.path.exists(windows_path):
        return windows_path

    raise RuntimeError("ffmpeg executable not found")


def _run(cmd: list[str]) -> None:
    """Run *cmd* raising :class:`FFMpegError` on failure."""

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as exc:  # pragma: no cover - exercised in tests
        raise FFMpegError(exc.stderr.decode("utf-8", "ignore")) from exc


def pngs_to_mp4(frames_dir: str | Path, fps: int, out_mp4: str | Path) -> Path:
    """Assemble a directory of PNG frames into a H.264 MP4 file.

    Parameters
    ----------
    frames_dir:
        Directory containing ``%04d.png`` style numbered frames.
    fps:
        Frame rate of the output video.
    out_mp4:
        Destination file path.
    """

    ffmpeg = find_ffmpeg()
    frames = Path(frames_dir)
    out_mp4 = Path(out_mp4)

    cmd = [
        ffmpeg,
        "-y",
        "-framerate",
        str(fps),
        "-i",
        str(frames / "%04d.png"),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(out_mp4),
    ]
    _run(cmd)
    return out_mp4


def mux_video_with_audio(
    video_silent: str | Path,
    source: str | Path,
    start_s: float,
    dur_s: float,
    out_mp4: str | Path,
) -> Path:
    """Mux ``video_silent`` with an audio segment from ``source``.

    The function tries three strategies as described in the project
    specification.  The first two strategies reuse audio from ``source``.
    If they fail a final attempt creates a silent audio track to ensure
    ``out_mp4`` is always produced.
    """

    ffmpeg = find_ffmpeg()
    video_silent = Path(video_silent)
    source = Path(source)
    out_mp4 = Path(out_mp4)

    # Strategy 1: re-encode audio directly from source.
    cmd1 = [
        ffmpeg,
        "-y",
        "-i",
        str(video_silent),
        "-ss",
        str(start_s),
        "-t",
        str(dur_s),
        "-i",
        str(source),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-ar",
        "44100",
        "-ac",
        "2",
        str(out_mp4),
    ]
    try:
        _run(cmd1)
        return out_mp4
    except FFMpegError:
        pass  # fall back

    # Strategy 2: extract audio first then mux.
    with tempfile.TemporaryDirectory() as tmp:
        audio_tmp = Path(tmp) / "segment.m4a"
        cmd_extract = [
            ffmpeg,
            "-y",
            "-ss",
            str(start_s),
            "-t",
            str(dur_s),
            "-i",
            str(source),
            "-c:a",
            "aac",
            "-ar",
            "44100",
            "-ac",
            "2",
            str(audio_tmp),
        ]
        try:
            _run(cmd_extract)
            cmd_mux = [
                ffmpeg,
                "-y",
                "-i",
                str(video_silent),
                "-i",
                str(audio_tmp),
                "-c",
                "copy",
                str(out_mp4),
            ]
            _run(cmd_mux)
            return out_mp4
        except FFMpegError:
            pass  # fall back

    # Strategy 3: generate silence.
    with tempfile.TemporaryDirectory() as tmp:
        silence = Path(tmp) / "silence.m4a"
        make_silence(dur_s, silence)
        cmd_mux = [
            ffmpeg,
            "-y",
            "-i",
            str(video_silent),
            "-i",
            str(silence),
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            str(out_mp4),
        ]
        _run(cmd_mux)
    return out_mp4


def make_silence(duration: float, out_audio: str | Path) -> Path:
    """Generate a silent audio file of ``duration`` seconds.

    The file format is inferred from the ``out_audio`` extension (either
    ``.wav`` or ``.m4a``)."""

    ffmpeg = find_ffmpeg()
    out_audio = Path(out_audio)
    cmd = [
        ffmpeg,
        "-y",
        "-f",
        "lavfi",
        "-t",
        str(duration),
        "-i",
        "anullsrc=channel_layout=stereo:sample_rate=44100",
        str(out_audio),
    ]
    _run(cmd)
    return out_audio
