import pytest

from olhos_de_deus.models import Status
from olhos_de_deus.orchestrator import Orchestrator
from olhos_de_deus.planner import plan
from olhos_de_deus.router import route


def test_empty_mission_is_rejected():
    with pytest.raises(ValueError):
        plan("   ")


def test_code_mission_routes_to_codebase_intelligence():
    mission = plan("Analisar erro no repositorio")
    capabilities = [step.capability for step in mission.steps]
    assert "inspect_code" in capabilities
    assert route("inspect_code").name == "CODEBASE_INTELLIGENCE"


def test_android_mission_routes_to_mobile_operator():
    mission = plan("Testar aplicativo Android")
    capabilities = [step.capability for step in mission.steps]
    assert "android" in capabilities
    assert route("android").name == "MOBILE_OPERATOR"


def test_orchestrator_completes_dry_run_with_qa_gate():
    mission = Orchestrator().run("Corrigir bug no projeto")
    assert mission.status == Status.VERIFIED
    assert mission.complete
    assert all(step.evidence for step in mission.steps)


def test_executor_failure_stops_mission():
    def failing_executor(agent, step, mission):
        raise RuntimeError("boom")

    mission = Orchestrator(executor=failing_executor).run("Construir recurso")
    assert mission.status == Status.FAILED
    assert mission.steps[0].status == Status.FAILED
