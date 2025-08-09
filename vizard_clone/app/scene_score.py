"""Scene and activity scoring utilities.

Only a very small portion of the original project's functionality is
implemented: the :func:`pick_best_windows` function.  It operates on
pre-calculated motion and speech energy profiles and selects the best
non-overlapping windows according to the weighted score described in the
specification.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple


@dataclass
class Window:
    start: int
    end: int
    score: float


def pick_best_windows(
    duration: int,
    motion: Sequence[float],
    speech: Sequence[float],
    window_candidates: Sequence[int] = (60, 45, 30),
    step: int = 5,
    top_n: int = 5,
    min_gap: int = 2,
) -> List[Window]:
    """Return the top ``top_n`` scoring windows.

    Parameters
    ----------
    duration:
        Total duration of the media in seconds.
    motion, speech:
        Sequences containing per-second motion and speech energy values.
    window_candidates:
        Candidate window sizes in seconds.
    step:
        Step size for the sliding window.
    top_n:
        Maximum number of windows to return.
    min_gap:
        Minimum number of seconds between the end of one window and the
        start of another.
    """

    candidates: List[Window] = []
    for w in window_candidates:
        for start in range(0, max(0, duration - w) + 1, step):
            end = start + w
            motion_avg = sum(motion[start:end]) / w
            speech_avg = sum(speech[start:end]) / w
            score = 0.7 * motion_avg + 0.3 * speech_avg
            candidates.append(Window(start, end, score))

    # Sort by score descending
    candidates.sort(key=lambda w: w.score, reverse=True)

    picked: List[Window] = []
    for win in candidates:
        if len(picked) >= top_n:
            break
        if all(win.end + min_gap <= p.start or win.start >= p.end + min_gap for p in picked):
            picked.append(win)

    # Sort picked windows chronologically for convenience
    picked.sort(key=lambda w: w.start)
    return picked


# The following functions are placeholders to maintain the module
# interface.  They are intentionally simplified and are not used in the
# unit tests, but they provide starting points for future development.

def detect_scenes(path: str, threshold: float) -> Iterable[Tuple[int, int]]:
    """Placeholder scene detection returning a single full-range scene."""
    # In a full implementation we would call PySceneDetect here.
    raise NotImplementedError("Scene detection is not implemented in this kata")


def motion_profile(path: str, start_s: float, end_s: float, fps: int, stride_frames: int):
    raise NotImplementedError


def speech_energy(path: str, start_s: float, end_s: float):
    raise NotImplementedError
