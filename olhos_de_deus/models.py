from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from uuid import uuid4


class Status(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    VERIFIED = "verified"
    FAILED = "failed"


@dataclass(slots=True)
class Step:
    name: str
    capability: str
    status: Status = Status.PENDING
    evidence: list[str] = field(default_factory=list)
    error: str | None = None


@dataclass(slots=True)
class Mission:
    request: str
    id: str = field(default_factory=lambda: uuid4().hex[:12])
    status: Status = Status.PENDING
    steps: list[Step] = field(default_factory=list)

    @property
    def complete(self) -> bool:
        return bool(self.steps) and all(step.status == Status.VERIFIED for step in self.steps)
