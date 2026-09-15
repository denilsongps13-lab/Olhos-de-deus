from pathlib import Path

import olhos_de_deus.ruflo as ruflo_module
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
