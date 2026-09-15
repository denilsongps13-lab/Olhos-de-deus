import json

import pytest

import olhos_de_deus.ruflo as ruflo_module
from olhos_de_deus.cli import _run_ruflo, build_parser
from olhos_de_deus.ruflo import RufloAdapter


def test_ruflo_is_phase_zero_and_external(tmp_path):
    adapter = RufloAdapter(tmp_path)
    report = adapter.report()
    assert report.phase == 0
    assert report.name == "ruflo"
    assert report.mode == "meta-harness"
    assert not report.operational


def test_ruflo_commands_use_npx_without_shell(tmp_path, monkeypatch):
    monkeypatch.setattr(
        ruflo_module.shutil,
        "which",
        lambda name: f"C:/tools/{name}.cmd" if name == "npx" else ("C:/tools/node.exe" if name == "node" else None),
    )
    adapter = RufloAdapter(tmp_path)
    assert adapter.build_init_command() == (
        "C:/tools/npx.cmd",
        "--yes",
        "ruflo@latest",
        "init",
    )
    assert adapter.build_wizard_command()[-2:] == ("init", "wizard")
    assert adapter.build_mcp_command()[-2:] == ("mcp", "start")
    assert adapter.init_workspace(dry_run=True) == adapter.build_init_command()


def test_ruflo_report_ready_after_workspace_initialized(tmp_path, monkeypatch):
    monkeypatch.setattr(
        ruflo_module.shutil,
        "which",
        lambda name: f"/tools/{name}" if name in {"node", "npx"} else None,
    )
    (tmp_path / ".claude-flow").mkdir()
    report = RufloAdapter(tmp_path).report()
    assert report.installed
    assert report.operational
    assert "workspace ready" in report.detail
    assert "no swarm started" in report.detail


def test_ruflo_swarm_commands_are_argument_safe(tmp_path, monkeypatch):
    monkeypatch.setattr(
        ruflo_module.shutil,
        "which",
        lambda name: f"C:/tools/{name}.cmd" if name == "npx" else ("C:/tools/node.exe" if name == "node" else None),
    )
    adapter = RufloAdapter(tmp_path)
    command = adapter.build_swarm_init_command(
        topology="hierarchical-mesh",
        max_agents=7,
        strategy="development",
        permissions="standard",
    )
    assert command[:4] == ("C:/tools/npx.cmd", "--yes", "ruflo@latest", "swarm")
    assert "--max-agents" in command
    assert command[command.index("--max-agents") + 1] == "7"
    assert command[-2:] == ("--format", "json")

    objective = 'Analyze repo; echo "not a shell command" && whoami'
    start = adapter.build_swarm_start_command(objective, strategy="analysis")
    assert objective in start
    assert start[start.index("--objective") + 1] == objective
    assert start[-2:] == ("--format", "json")


def test_ruflo_swarm_validation_rejects_unsupported_options(tmp_path):
    adapter = RufloAdapter(tmp_path)
    with pytest.raises(ValueError):
        adapter.build_swarm_init_command(topology="unknown")
    with pytest.raises(ValueError):
        adapter.build_swarm_init_command(max_agents=99)
    with pytest.raises(ValueError):
        adapter.build_swarm_init_command(permissions="root")
    with pytest.raises(ValueError):
        adapter.build_swarm_start_command("mission", strategy="anything")
    with pytest.raises(ValueError):
        adapter.build_swarm_start_command("   ")


def test_ruflo_swarm_execution_requires_initialized_workspace(tmp_path, monkeypatch):
    monkeypatch.setattr(
        ruflo_module.shutil,
        "which",
        lambda name: f"/tools/{name}" if name in {"node", "npx"} else None,
    )
    adapter = RufloAdapter(tmp_path)
    with pytest.raises(RuntimeError, match="Initialize the Ruflo workspace"):
        adapter.init_swarm(dry_run=False)
    with pytest.raises(RuntimeError, match="Initialize the Ruflo workspace"):
        adapter.start_swarm("Analyze code", dry_run=False)


def test_ruflo_swarm_dry_runs_do_not_need_node_or_network(tmp_path):
    adapter = RufloAdapter(tmp_path)
    init_command = adapter.init_swarm(dry_run=True)
    start_command = adapter.start_swarm("Analyze code", dry_run=True)
    status_command = adapter.swarm_status(dry_run=True)
    assert init_command[-2:] == ("--format", "json")
    assert "Analyze code" in start_command
    assert status_command[-4:] == ("swarm", "status", "--format", "json")


def test_ruflo_cli_init_is_dry_run_by_default(tmp_path, capsys):
    args = build_parser().parse_args(["ruflo", "init", "--workspace", str(tmp_path)])
    assert args.command == "ruflo"
    assert args.ruflo_command == "init"
    _run_ruflo(args)
    payload = json.loads(capsys.readouterr().out)
    assert payload["phase"] == 0
    assert payload["execute"] is False
    assert payload["command"][-2:] == ["ruflo@latest", "init"]


def test_doctor_can_include_ruflo_without_changing_seven_phase_hub(tmp_path):
    args = build_parser().parse_args(
        [
            "doctor",
            "--external-root",
            str(tmp_path),
            "--with-ruflo",
            "--ruflo-workspace",
            str(tmp_path),
            "--json",
        ]
    )
    assert args.with_ruflo is True
    assert args.ruflo_workspace == str(tmp_path)
