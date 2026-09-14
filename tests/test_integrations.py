from pathlib import Path

import pytest

import olhos_de_deus.integrations as integrations
from olhos_de_deus.integrations import (
    ADHDOutputAdapter,
    AgencyAgentsAdapter,
    ArtemisAdapter,
    GraphifyAdapter,
    IntegrationHub,
    QASkillsAdapter,
    SpecKitAdapter,
)


def _prepare_external(root: Path) -> None:
    qa_skill = root / "qa-skills" / "skills" / "unit-testing" / "SKILL.md"
    qa_skill.parent.mkdir(parents=True)
    qa_skill.write_text("# Unit testing", encoding="utf-8")

    adhd = root / "i-have-adhd" / "skills" / "i-have-adhd" / "SKILL.md"
    adhd.parent.mkdir(parents=True)
    adhd.write_text("Lead with the next action.", encoding="utf-8")

    agent = root / "agency-agents" / "engineering" / "engineering-backend-architect.md"
    agent.parent.mkdir(parents=True)
    agent.write_text("# Backend Architect", encoding="utf-8")

    artemis = root / "artemis" / "pyproject.toml"
    artemis.parent.mkdir(parents=True)
    artemis.write_text("[project]\nname='artemis'\n", encoding="utf-8")

    for name in ("graphify", "comfyui", "spec-kit"):
        (root / name).mkdir(parents=True, exist_ok=True)


def test_hub_has_exactly_seven_ordered_phases(tmp_path):
    _prepare_external(tmp_path)
    hub = IntegrationHub(tmp_path)
    reports = hub.reports()
    assert len(reports) == 7
    assert [item.phase for item in reports] == list(range(1, 8))
    assert hub.names() == (
        "graphify",
        "comfyui",
        "spec-kit",
        "qa-skills",
        "i-have-adhd",
        "agency-agents",
        "artemis",
    )


def test_content_adapters_load_upstream_material(tmp_path):
    _prepare_external(tmp_path)
    assert QASkillsAdapter(tmp_path).list_skills() == ("unit-testing",)
    assert "Unit testing" in QASkillsAdapter(tmp_path).load_skill("unit-testing")
    assert "next action" in ADHDOutputAdapter(tmp_path).load_rules()
    agency = AgencyAgentsAdapter(tmp_path)
    assert "engineering-backend-architect" in agency.list_agents()
    assert "Backend Architect" in agency.load_agent("backend")


def test_cli_adapters_build_official_commands(tmp_path, monkeypatch):
    _prepare_external(tmp_path)

    def fake_which(name):
        return f"/tools/{name}" if name in {"graphify", "specify", "uv"} else None

    monkeypatch.setattr(integrations.shutil, "which", fake_which)

    graphify = GraphifyAdapter(tmp_path)
    assert graphify.report().operational
    assert graphify.run(".", dry_run=True) == ("graphify", ".")

    spec = SpecKitAdapter(tmp_path)
    assert spec.report().operational
    assert spec.init_project(tmp_path, dry_run=True) == (
        "specify",
        "init",
        "--here",
        "--force",
        "--non-interactive",
        "--integration",
        "copilot",
    )

    artemis = ArtemisAdapter(tmp_path)
    assert artemis.report().operational
    assert artemis.run("Open Settings", dry_run=True) == (
        "uv",
        "run",
        "artemis",
        "run",
        "Open Settings",
        "--profile",
        "flash",
    )


def test_missing_content_fails_clearly(tmp_path):
    with pytest.raises(KeyError):
        QASkillsAdapter(tmp_path).load_skill("missing")
    with pytest.raises(FileNotFoundError):
        ADHDOutputAdapter(tmp_path).load_rules()
    with pytest.raises(KeyError):
        AgencyAgentsAdapter(tmp_path).find_agent("backend")


def test_doctor_without_external_repos_is_safe(tmp_path):
    reports = IntegrationHub(tmp_path).reports()
    assert len(reports) == 7
    assert not any(report.operational for report in reports)
