"""Command line interface for vizard_clone (minimal)."""
from __future__ import annotations

import argparse
from pathlib import Path

from .app import pipeline


def cmd_process(args: argparse.Namespace) -> None:
    for video in args.videos:
        out_dir = Path(args.out_dir or pipeline.config.PROCESSED)
        pipeline.process_video(video, out_dir)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="vizard_clone")
    sub = parser.add_subparsers(dest="command")

    p_process = sub.add_parser("process", help="process input videos")
    p_process.add_argument("videos", nargs="+", help="input video files")
    p_process.add_argument("--out-dir", default=None)
    p_process.set_defaults(func=cmd_process)

    args = parser.parse_args(argv)
    if hasattr(args, "func"):
        args.func(args)
        return 0
    parser.print_help()
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
