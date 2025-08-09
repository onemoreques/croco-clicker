"""Minimal Flask preview application."""
from __future__ import annotations

from pathlib import Path
from typing import List

from flask import Flask, send_from_directory

app = Flask(__name__)


@app.route("/clips/<path:name>")
def clips(name: str):
    directory = Path(name).parent
    filename = Path(name).name
    return send_from_directory(directory, filename)


# The full implementation would list clips and provide approval toggles.
# For the purposes of this kata the Flask app only exposes a static file
# endpoint so other modules can import ``app`` without side effects.
