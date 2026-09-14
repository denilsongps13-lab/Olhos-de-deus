from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Agent:
    name: str
    capabilities: frozenset[str]


AGENTS = (
    Agent("ARCHITECT", frozenset({"specify", "plan"})),
    Agent("CODEBASE_INTELLIGENCE", frozenset({"inspect_code"})),
    Agent("BUILDER", frozenset({"implement"})),
    Agent("GUARDIAN_QA", frozenset({"verify", "test"})),
    Agent("MOBILE_OPERATOR", frozenset({"android"})),
)


def route(capability: str) -> Agent:
    for agent in AGENTS:
        if capability in agent.capabilities:
            return agent
    raise LookupError(f"No agent registered for capability: {capability}")
