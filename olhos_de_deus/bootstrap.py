from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .sources import select_sources


@dataclass(frozen=True, slots=True)
class BootstrapResult:
    source: str
    action: str
    path: str
    command: tuple[str, ...]


def _run(command: list[str], cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def bootstrap_sources(
    target: str | Path = "external",
    names: Iterable[str] | None = None,
    *,
    dry_run: bool = False,
) -> tuple[BootstrapResult, ...]:
    if shutil.which("git") is None and not dry_run:
        raise RuntimeError("Git is required to bootstrap upstream repositories")

    destination = Path(target).expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    results: list[BootstrapResult] = []

    for source in select_sources(names):
        repo_path = destination / source.name
        if not repo_path.exists():
            command = [
                "git", "clone", "--depth", "1", "--branch", source.ref,
                source.clone_url, str(repo_path),
            ]
            action = "clone"
            if not dry_run:
                _run(command)
        elif (repo_path / ".git").exists():
            command = ["git", "pull", "--ff-only", "origin", source.ref]
            action = "update"
            if not dry_run:
                _run(["git", "fetch", "origin", source.ref], repo_path)
                _run(["git", "checkout", source.ref], repo_path)
                _run(command, repo_path)
        else:
            raise RuntimeError(f"Refusing to overwrite non-git directory: {repo_path}")

        results.append(BootstrapResult(source.name, action, str(repo_path), tuple(command)))

    return tuple(results)
