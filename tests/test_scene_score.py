from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from vizard_clone.app.scene_score import pick_best_windows


def test_pick_best_windows_simple():
    duration = 40
    motion = [1] * 10 + [0] * 10 + [1] * 10 + [0] * 10
    speech = [0] * 40
    wins = pick_best_windows(
        duration,
        motion,
        speech,
        window_candidates=[10],
        step=5,
        top_n=2,
    )
    assert [(w.start, w.end) for w in wins] == [(0, 10), (20, 30)]
