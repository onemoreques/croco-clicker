"""YouTube uploader stub."""
from __future__ import annotations

from pathlib import Path


def upload(path: str | Path, title: str, description: str, tags: list[str]) -> dict:
    """Pretend to upload *path* returning a dummy response."""
    return {"id": "stub", "title": title}
