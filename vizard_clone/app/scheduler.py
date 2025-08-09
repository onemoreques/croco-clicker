"""Simple scheduling stub using APScheduler."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List

try:  # pragma: no cover - APScheduler is optional for tests
    from apscheduler.schedulers.background import BackgroundScheduler
except Exception:  # pragma: no cover
    BackgroundScheduler = None  # type: ignore

from .uploader import upload


@dataclass
class Job:
    when: datetime
    path: str
    title: str
    description: str
    tags: List[str]


class Scheduler:
    def __init__(self):
        self.jobs: List[Job] = []
        self.scheduler = BackgroundScheduler() if BackgroundScheduler else None

    def add(self, job: Job):
        self.jobs.append(job)

    def run_pending(self):
        for job in list(self.jobs):
            if job.when <= datetime.utcnow():
                upload(job.path, job.title, job.description, job.tags)
                self.jobs.remove(job)
