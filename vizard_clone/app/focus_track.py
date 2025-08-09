"""Focus tracking placeholder implementation.

The real project computes saliency and motion based attention maps to
produce a smooth virtual camera path.  Implementing this would require a
number of heavy dependencies.  For the sake of the exercises this module
contains lightweight stubs that document the intended interface.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


dataclass = dataclass  # re-export for type checkers


@dataclass
class FocusPoint:
    x: float
    y: float
    zoom: float


def compute_focus_path(num_frames: int, width: int, height: int) -> List[FocusPoint]:
    """Return a list of ``FocusPoint`` objects describing the camera path.

    The stub simply centres the focus and applies a constant zoom of 1.0.
    It is sufficient for tests that rely on deterministic behaviour.
    """

    return [FocusPoint(width / 2, height / 2, 1.0) for _ in range(num_frames)]
