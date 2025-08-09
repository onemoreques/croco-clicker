"""Application configuration constants.

The real project would likely load many of these from environment
variables.  For the purposes of this kata the values are mostly static
so unit tests can rely on deterministic behaviour.
"""
from __future__ import annotations

import os
from dataclasses import dataclass


INCOMING = "incoming"
PROCESSED = "processed"
LOGS = "logs"
TEMP = "temp"

TARGET_W = 1080
TARGET_H = 1920
ASPECT = 9 / 16
TOP_N = 5
WINDOW_CANDIDATES = (60, 45, 30)
STEP = 5
SCENE_THRESHOLD = 27.0
SAMPLE_HZ = 6
SMOOTH_SEC = 0.5
ZOOM_MIN = 1.00
ZOOM_MAX = 1.10
ZOOM_PERIOD = 6.0

PRENORMALIZE = True
AUTO_FFMPEG = True
FFMPEG_PATH = None  # optional manual override

WHISPER_MODEL = "small"
LANG_AUTO = True

TTS_ENGINE = os.getenv("TTS_ENGINE", "edge")
TTS_VOICE = os.getenv("TTS_VOICE", "ru-RU-DariyaNeural")

TRANSLATE_ENGINE = os.getenv("TRANSLATE_ENGINE", "argos")

# YouTube / uploader settings
YTB_CLIENT_SECRET_FILE = os.getenv("YTB_CLIENT_SECRET_FILE")
YTB_SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CHANNEL_ID = os.getenv("CHANNEL_ID")
AUTO_UPLOAD = False
REQUIRE_APPROVAL = True


@dataclass
class MetadataTemplates:
    """Metadata template placeholders used by the scheduler/uploader.

    The templates intentionally use Python's ``str.format`` syntax.  See
    README for available fields.
    """

    title: str = "{base_title}"
    description: str = "{source_name} @ {start_mmss}"
    tags: str = "shorts"


META_TEMPLATES = MetadataTemplates()
