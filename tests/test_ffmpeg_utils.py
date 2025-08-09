import subprocess
from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))
from vizard_clone.app.ffmpeg_utils import find_ffmpeg, mux_video_with_audio


def _sample_inputs(tmp_path: Path):
    try:
        ffmpeg = find_ffmpeg()
    except RuntimeError:
        pytest.skip("ffmpeg not installed")
    video = tmp_path / "video.mp4"
    audio = tmp_path / "audio.m4a"
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=c=black:s=160x90:d=1",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(video),
        ],
        check=True,
    )
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=1000:duration=1",
            "-c:a",
            "aac",
            str(audio),
        ],
        check=True,
    )
    return video, audio


def test_mux_with_audio(tmp_path: Path):
    video, audio = _sample_inputs(tmp_path)
    out = tmp_path / "out.mp4"
    mux_video_with_audio(video, audio, 0, 1, out)
    assert out.exists() and out.stat().st_size > 0


def test_mux_with_missing_audio(tmp_path: Path):
    video, audio = _sample_inputs(tmp_path)
    out = tmp_path / "out_silence.mp4"
    mux_video_with_audio(video, tmp_path / "missing.m4a", 0, 1, out)
    assert out.exists() and out.stat().st_size > 0
