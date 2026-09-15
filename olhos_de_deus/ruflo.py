from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from .integrations import IntegrationReport


class RufloAdapter:
    """Optional phase-zero meta-harness around the seven Olhos de Deus phases.

    Ruflo stays external to the core. The adapter only builds and executes the
    official npx commands without shell=True and never installs silently.
    """

    phase = 0
    name = "ruflo"
    mode = "meta-harness"

    def __init__(self, workspace: str | Path = ".") -> None:
        self.workspace = Path(workspace).expanduser().resolve()

    @property
    def node_path(self) -> str | None:
        return shutil.which("node")

    @property
    def npx_path(self) -> str | None:
        return shutil.which("npx")

    @property
    def initialized(self) -> bool:
        return (self.workspace / ".claude-flow").exists()

    def report(self) -> IntegrationReport:
        installed = self.npx_path is not None and self.node_path is not None
        operational = installed and self.initialized
        if operational:
            detail = f"Ruflo workspace ready: {self.workspace}"
        elif not installed:
            detail = "Node.js/npx not found. Install Node.js before enabling Ruflo."
        else:
            detail = f"Node.js/npx ready; Ruflo is not initialized in {self.workspace}."
        return IntegrationReport(
            phase=self.phase,
            name=self.name,
            mode=self.mode,
            installed=installed,
            operational=operational,
            detail=detail,
        )

    def build_init_command(self) -> tuple[str, ...]:
        executable = self.npx_path or "npx"
        return (executable, "--yes", "ruflo@latest", "init")

    def build_wizard_command(self) -> tuple[str, ...]:
        executable = self.npx_path or "npx"
        return (executable, "--yes", "ruflo@latest", "init", "wizard")

    def build_mcp_command(self) -> tuple[str, ...]:
        executable = self.npx_path or "npx"
        return (executable, "--yes", "ruflo@latest", "mcp", "start")

    def build_version_command(self) -> tuple[str, ...]:
        executable = self.npx_path or "npx"
        return (executable, "--yes", "ruflo@latest", "--version")

    def init_workspace(
        self,
        *,
        wizard: bool = False,
        dry_run: bool = True,
        timeout: float = 180.0,
    ) -> subprocess.CompletedProcess[str] | tuple[str, ...]:
        command = self.build_wizard_command() if wizard else self.build_init_command()
        if dry_run:
            return command
        if self.npx_path is None or self.node_path is None:
            raise RuntimeError("Node.js and npx are required to initialize Ruflo")
        self.workspace.mkdir(parents=True, exist_ok=True)
        return subprocess.run(
            command,
            cwd=self.workspace,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

    def probe_runtime(
        self,
        *,
        dry_run: bool = True,
        timeout: float = 60.0,
    ) -> subprocess.CompletedProcess[str] | tuple[str, ...]:
        command = self.build_version_command()
        if dry_run:
            return command
        if self.npx_path is None or self.node_path is None:
            raise RuntimeError("Node.js and npx are required to probe Ruflo")
        return subprocess.run(
            command,
            cwd=self.workspace if self.workspace.exists() else None,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
