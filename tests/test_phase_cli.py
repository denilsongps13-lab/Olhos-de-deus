import json

import pytest

from olhos_de_deus.cli import _run_phase, build_parser


@pytest.mark.parametrize(
    ("argv", "phase_name"),
    [
        (["phase", "graphify"], "graphify"),
        (["phase", "comfyui"], "comfyui"),
        (["phase", "spec-kit"], "spec-kit"),
        (["phase", "qa-skills"], "qa-skills"),
        (["phase", "i-have-adhd"], "i-have-adhd"),
        (["phase", "agency-agents"], "agency-agents"),
        (["phase", "artemis", "Open Settings"], "artemis"),
    ],
)
def test_all_seven_phase_commands_parse(argv, phase_name):
    args = build_parser().parse_args(argv)
    assert args.command == "phase"
    assert args.phase_name == phase_name


def test_graphify_phase_is_dry_run_by_default(tmp_path, capsys):
    args = build_parser().parse_args(
        ["phase", "graphify", ".", "--external-root", str(tmp_path)]
    )
    _run_phase(args)
    payload = json.loads(capsys.readouterr().out)
    assert payload["phase"] == 1
    assert payload["execute"] is False
    assert payload["command"] == ["graphify", "."]


def test_spec_kit_phase_is_dry_run_by_default(tmp_path, capsys):
    args = build_parser().parse_args(
        ["phase", "spec-kit", str(tmp_path), "--external-root", str(tmp_path)]
    )
    _run_phase(args)
    payload = json.loads(capsys.readouterr().out)
    assert payload["phase"] == 3
    assert payload["execute"] is False
    assert payload["command"][0:2] == ["specify", "init"]


def test_comfyui_workflow_can_be_validated_without_network(tmp_path, capsys):
    workflow = tmp_path / "workflow.json"
    workflow.write_text('{"1": {"class_type": "Example", "inputs": {}}}', encoding="utf-8")
    args = build_parser().parse_args(
        [
            "phase",
            "comfyui",
            "--workflow",
            str(workflow),
            "--external-root",
            str(tmp_path),
        ]
    )
    _run_phase(args)
    payload = json.loads(capsys.readouterr().out)
    assert payload["phase"] == 2
    assert payload["execute"] is False
    assert payload["nodes"] == 1


def test_artemis_phase_is_dry_run_by_default(tmp_path, capsys):
    args = build_parser().parse_args(
        [
            "phase",
            "artemis",
            "Open Settings",
            "--profile",
            "pro",
            "--external-root",
            str(tmp_path),
        ]
    )
    _run_phase(args)
    payload = json.loads(capsys.readouterr().out)
    assert payload["phase"] == 7
    assert payload["execute"] is False
    assert payload["command"][-2:] == ["--profile", "pro"]
