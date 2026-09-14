from __future__ import annotations

from .models import Mission, Status


class GuardianQA:
    """Final deterministic gate. Real test adapters will plug into this contract."""

    def verify(self, mission: Mission) -> tuple[bool, list[str]]:
        problems: list[str] = []
        for step in mission.steps[:-1]:
            if step.status != Status.VERIFIED:
                problems.append(f"{step.name}: status={step.status}")
            if not step.evidence:
                problems.append(f"{step.name}: missing evidence")
        return (not problems, problems)
