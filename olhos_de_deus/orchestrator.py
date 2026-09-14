from __future__ import annotations

from collections.abc import Callable

from .models import Mission, Status, Step
from .planner import plan
from .qa import GuardianQA
from .router import Agent, route

Executor = Callable[[Agent, Step, Mission], str]


def dry_run_executor(agent: Agent, step: Step, mission: Mission) -> str:
    return f"{agent.name} accepted '{step.name}' for mission {mission.id}"


class Orchestrator:
    def __init__(self, executor: Executor = dry_run_executor) -> None:
        self.executor = executor
        self.guardian = GuardianQA()

    def run(self, request: str) -> Mission:
        mission = plan(request)
        mission.status = Status.RUNNING

        for step in mission.steps[:-1]:
            step.status = Status.RUNNING
            try:
                agent = route(step.capability)
                evidence = self.executor(agent, step, mission)
                step.evidence.append(evidence)
                step.status = Status.VERIFIED
            except Exception as exc:
                step.error = str(exc)
                step.status = Status.FAILED
                mission.status = Status.FAILED
                return mission

        gate = mission.steps[-1]
        gate.status = Status.RUNNING
        passed, problems = self.guardian.verify(mission)
        if passed:
            gate.evidence.append("Guardian QA approved mission")
            gate.status = Status.VERIFIED
            mission.status = Status.VERIFIED
        else:
            gate.error = "; ".join(problems)
            gate.status = Status.FAILED
            mission.status = Status.FAILED
        return mission
