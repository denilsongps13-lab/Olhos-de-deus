import pytest

from olhos_de_deus.bootstrap import bootstrap_sources
from olhos_de_deus.sources import load_sources, select_sources


def test_manifest_contains_all_seven_sources():
    sources = load_sources()
    assert len(sources) == 7
    assert {source.name for source in sources} == {
        "graphify", "comfyui", "spec-kit", "qa-skills",
        "i-have-adhd", "agency-agents", "artemis",
    }


def test_select_unknown_source_fails():
    with pytest.raises(KeyError):
        select_sources(["does-not-exist"])


def test_bootstrap_dry_run_builds_safe_clone_command(tmp_path):
    result = bootstrap_sources(tmp_path, ["artemis"], dry_run=True)[0]
    assert result.action == "clone"
    assert result.command[:4] == ("git", "clone", "--depth", "1")
    assert "https://github.com/google/artemis.git" in result.command
