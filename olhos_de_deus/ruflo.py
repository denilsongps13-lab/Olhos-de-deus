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

    SWARM_TOPOLOGIES = {
        "hierarchical",
        "mesh",
        "ring",
        "star",
        "hybrid",
        "hierarchical-mesh",
        "pheromone-adaptive",
    }
    SWARM_STRATEGIES = {
        "specialized",
        "balanced",
        "adaptive",
        "research",
        "development",
        "testing",
        "optimization",
        "maintenance",
        "analysis",
    }
    PERMISSION_PRESETS = {"strict", "standard", "permissive"}

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

    @property
    def swarm_initialized(self) -> bool:
        return (self.workspace / ".swarm" / "state.json").is_file()

    def report(self) -> IntegrationReport:
        installed = self.npx_path is not None and self.node_path is not None
        operational = installed and self.initialized
        if operational:
            swarm = "; swarm state available" if self.swarm_initialized else "; no swarm started"
            detail = f"Ruflo workspace ready: {self.workspace}{swarm}"
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

    def _npx_prefix(self) -> tuple[str, ...]:
        return (self.npx_path or "npx", "--yes", "ruflo@latest")

    def _ensure_runtime(self) -> None:
        if self.npx_path is None or self.node_path is None:
            raise RuntimeError("Node.js and npx are required to use Ruflo")

    def _ensure_workspace(self) -> None:
        self.workspace.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _validate_strategy(cls, strategy: str) -> str:
        value = strategy.strip().lower()
        if value not in cls.SWARM_STRATEGIES:
            raise ValueError(f"Unsupported Ruflo swarm strategy: {strategy}")
        return value

    @classmethod
    def _validate_topology(cls, topology: str) -> str:
        value = topology.strip().lower()
        if value not in cls.SWARM_TOPOLOGIES:
            raise ValueError(f"Unsupported Ruflo swarm topology: {topology}")
        return value

    @classmethod
    def _validate_permissions(cls, permissions: str) -> str:
        value = permissions.strip().lower()
        if value not in cls.PERMISSION_PRESETS:
            raise ValueError(f"Unsupported Ruflo permission preset: {permissions}")
        return value

    @staticmethod
    def _validate_agents(max_agents: int) -> int:
        value = int(max_agents)
        if not 1 <= value <= 15:
            raise ValueError("Ruflo max_agents must be between 1 and 15")
        return value

    @staticmethod
    def _validate_objective(objective: str) -> str:
        value = objective.strip()
        if not value:
            raise ValueError("Ruflo swarm objective cannot be empty")
        if len(value) > 4000:
            raise ValueError("Ruflo swarm objective is too long (maximum 4000 characters)")
        return value

    def build_init_command(self) -> tuple[str, ...]:
        return (*self._npx_prefix(), "init")

    def build_wizard_command(self) -> tuple[str, ...]:
        return (*self._npx_prefix(), "init", "wizard")

    def build_mcp_command(self) -> tuple[str, ...]:
        return (*self._npx_prefix(), "mcp", "start")

    def build_version_command(self) -> tuple[str, ...]:
        return (*self._npx_prefix(), "--version")

    def build_swarm_init_command(
        self,
        *,
        topology: str = "hierarchical",
        max_agents: int = 7,
        strategy: str = "development",
        permissions: str = "standard",
    ) -> tuple[str, ...]:
        topology = self._validate_topology(topology)
        strategy = self._validate_strategy(strategy)
        permissions = self._validate_permissions(permissions)
        max_agents = self._validate_agents(max_agents)
        return (
            *self._npx_prefix(),
            "swarm",
            "init",
            "--topology",
            topology,
            "--max-agents",
            str(max_agents),
            "--strategy",
            strategy,
            "--with-permissions",
            permissions,
            "--format",
            "json",
        )

    def build_swarm_start_command(
        self,
        objective: str,
        *,
        strategy: str = "development",
    ) -> tuple[str, ...]:
        objective = self._validate_objective(objective)
        strategy = self._validate_strategy(strategy)
        return (
            *self._npx_prefix(),
            "swarm",
            "start",
            "--objective",
            objective,
            "--strategy",
            strategy,
            "--format",
            "json",
        )

    def build_swarm_status_command(self) -> tuple[str, ...]:
        return (*self._npx_prefix(), "swarm", "status", "--format", "json")

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
        self._ensure_runtime()
        self._ensure_workspace()
        return subprocess.run(
            command,
            cwd=self.workspace,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

    def init_swarm(
        self,
        *,
        topology: str = "hierarchical",
        max_agents: int = 7,
        strategy: str = "development",
        permissions: str = "standard",
        dry_run: bool = True,
        timeout: float = 180.0,
    ) -> subprocess.CompletedProcess[str] | tuple[str, ...]:
        command = self.build_swarm_init_command(
            topology=topology,
            max_agents=max_agents,
            strategy=strategy,
            permissions=permissions,
        )
        if dry_run:
            return command
        self._ensure_runtime()
        if not self.initialized:
            raise RuntimeError("Initialize the Ruflo workspace before creating a swarm")
        return subprocess.run(
            command,
            cwd=self.workspace,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

    def start_swarm(
        self,
        objective: str,
        *,
        strategy: str = "development",
        dry_run: bool = True,
        timeout: float = 180.0,
    ) -> subprocess.CompletedProcess[str] | tuple[str, ...]:
        command = self.build_swarm_start_command(objective, strategy=strategy)
        if dry_run:
            return command
        self._ensure_runtime()
        if not self.initialized:
            raise RuntimeError("Initialize the Ruflo workspace before starting a swarm")
        return subprocess.run(
            command,
            cwd=self.workspace,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

    def swarm_status(
        self,
        *,
        dry_run: bool = True,
        timeout: float = 60.0,
    ) -> subprocess.CompletedProcess[str] | tuple[str, ...]:
        command = self.build_swarm_status_command()
        if dry_run:
            return command
        self._ensure_runtime()
        if not self.initialized:
            raise RuntimeError("Initialize the Ruflo workspace before querying swarm status")
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
        self._ensure_runtime()
        return subprocess.run(
            command,
            cwd=self.workspace if self.workspace.exists() else None,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
