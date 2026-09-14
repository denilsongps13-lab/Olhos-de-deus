from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class IntegrationReport:
    phase: int
    name: str
    mode: str
    installed: bool
    operational: bool
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class IntegrationAdapter:
    phase: int = 0
    name: str = ""
    mode: str = ""
    directory: str = ""

    def __init__(self, external_root: str | Path = "external") -> None:
        self.external_root = Path(external_root).expanduser().resolve()

    @property
    def repo_path(self) -> Path:
        return self.external_root / (self.directory or self.name)

    @property
    def installed(self) -> bool:
        return self.repo_path.exists()

    def report(self, *, probe_services: bool = False) -> IntegrationReport:
        raise NotImplementedError


class GraphifyAdapter(IntegrationAdapter):
    phase = 1
    name = "graphify"
    mode = "local-cli"

    def report(self, *, probe_services: bool = False) -> IntegrationReport:
        executable = shutil.which("graphify")
        operational = executable is not None
        if operational:
            detail = f"CLI ready: {executable}"
        elif self.installed:
            detail = "Repository cloned; install graphifyy to expose the graphify CLI."
        else:
            detail = "Not bootstrapped yet."
        return IntegrationReport(self.phase, self.name, self.mode, self.installed, operational, detail)

    def build_command(self, target: str | Path = ".") -> tuple[str, ...]:
        return ("graphify", str(target))

    def run(self, target: str | Path = ".", *, dry_run: bool = False) -> subprocess.CompletedProcess[str] | tuple[str, ...]:
        command = self.build_command(target)
        if dry_run:
            return command
        if shutil.which("graphify") is None:
            raise RuntimeError("graphify CLI is not installed; install the official graphifyy package first")
        return subprocess.run(command, check=True, capture_output=True, text=True)


class ComfyUIAdapter(IntegrationAdapter):
    phase = 2
    name = "comfyui"
    mode = "external-http-api"

    def __init__(self, external_root: str | Path = "external", endpoint: str | None = None) -> None:
        super().__init__(external_root)
        self.endpoint = (endpoint or os.getenv("COMFYUI_URL") or "http://127.0.0.1:8188").rstrip("/")

    def _request_json(
        self,
        path: str,
        *,
        method: str = "GET",
        payload: dict[str, Any] | None = None,
        timeout: float = 3.0,
    ) -> Any:
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = Request(
            f"{self.endpoint}{path}",
            data=data,
            method=method,
            headers={"Content-Type": "application/json"},
        )
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}

    def report(self, *, probe_services: bool = False) -> IntegrationReport:
        operational = False
        detail = f"API configured at {self.endpoint}; service probe not requested."
        if probe_services:
            try:
                self._request_json("/system_stats", timeout=2.0)
                operational = True
                detail = f"ComfyUI API reachable at {self.endpoint}."
            except (OSError, URLError, ValueError) as exc:
                detail = f"ComfyUI API not reachable at {self.endpoint}: {exc}"
        return IntegrationReport(self.phase, self.name, self.mode, self.installed, operational, detail)

    def queue_prompt(
        self,
        workflow: dict[str, Any],
        *,
        client_id: str | None = None,
        timeout: float = 30.0,
    ) -> Any:
        if not isinstance(workflow, dict) or not workflow:
            raise ValueError("workflow must be a non-empty ComfyUI API-format dictionary")
        payload = {"prompt": workflow, "client_id": client_id or uuid4().hex}
        return self._request_json("/prompt", method="POST", payload=payload, timeout=timeout)


class SpecKitAdapter(IntegrationAdapter):
    phase = 3
    name = "spec-kit"
    mode = "local-cli"

    def report(self, *, probe_services: bool = False) -> IntegrationReport:
        executable = shutil.which("specify")
        operational = executable is not None
        if operational:
            detail = f"Specify CLI ready: {executable}"
        elif self.installed:
            detail = "Repository cloned; install specify-cli to execute Spec Kit commands."
        else:
            detail = "Not bootstrapped yet."
        return IntegrationReport(self.phase, self.name, self.mode, self.installed, operational, detail)

    def init_command(self, integration: str = "copilot") -> tuple[str, ...]:
        if not integration.strip():
            raise ValueError("integration cannot be empty")
        return (
            "specify",
            "init",
            "--here",
            "--force",
            "--non-interactive",
            "--integration",
            integration,
        )

    def init_project(
        self,
        target: str | Path,
        *,
        integration: str = "copilot",
        dry_run: bool = False,
    ) -> subprocess.CompletedProcess[str] | tuple[str, ...]:
        command = self.init_command(integration)
        if dry_run:
            return command
        if shutil.which("specify") is None:
            raise RuntimeError("specify CLI is not installed")
        cwd = Path(target).expanduser().resolve()
        cwd.mkdir(parents=True, exist_ok=True)
        return subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)


class QASkillsAdapter(IntegrationAdapter):
    phase = 4
    name = "qa-skills"
    mode = "agent-skills"

    @property
    def skills_root(self) -> Path:
        return self.repo_path / "skills"

    def skill_files(self) -> tuple[Path, ...]:
        if not self.skills_root.exists():
            return ()
        return tuple(sorted(self.skills_root.glob("*/SKILL.md")))

    def list_skills(self) -> tuple[str, ...]:
        return tuple(path.parent.name for path in self.skill_files())

    def load_skill(self, name: str) -> str:
        path = self.skills_root / name / "SKILL.md"
        if not path.is_file():
            raise KeyError(f"QA skill not found: {name}")
        return path.read_text(encoding="utf-8")

    def report(self, *, probe_services: bool = False) -> IntegrationReport:
        count = len(self.skill_files())
        operational = count > 0
        detail = f"{count} QA skill(s) available." if operational else "QA skills are not available locally."
        return IntegrationReport(self.phase, self.name, self.mode, self.installed, operational, detail)


class ADHDOutputAdapter(IntegrationAdapter):
    phase = 5
    name = "i-have-adhd"
    mode = "output-profile"

    @property
    def skill_file(self) -> Path:
        return self.repo_path / "skills" / "i-have-adhd" / "SKILL.md"

    def load_rules(self) -> str:
        if not self.skill_file.is_file():
            raise FileNotFoundError(self.skill_file)
        return self.skill_file.read_text(encoding="utf-8")

    def report(self, *, probe_services: bool = False) -> IntegrationReport:
        operational = self.skill_file.is_file()
        detail = "Output profile ready." if operational else "Output profile skill file not found."
        return IntegrationReport(self.phase, self.name, self.mode, self.installed, operational, detail)


class AgencyAgentsAdapter(IntegrationAdapter):
    phase = 6
    name = "agency-agents"
    mode = "agent-catalog"

    _ignored_roots = {".github", "docs", "scripts", "integrations", "assets"}

    def agent_files(self) -> tuple[Path, ...]:
        if not self.repo_path.exists():
            return ()
        files: list[Path] = []
        for path in self.repo_path.glob("*/*.md"):
            relative = path.relative_to(self.repo_path)
            if relative.parts[0] in self._ignored_roots:
                continue
            if path.name.casefold().startswith("readme"):
                continue
            files.append(path)
        return tuple(sorted(files))

    def list_agents(self) -> tuple[str, ...]:
        return tuple(path.stem for path in self.agent_files())

    def find_agent(self, query: str) -> Path:
        needle = query.casefold().replace(" ", "-").strip()
        if not needle:
            raise ValueError("query cannot be empty")
        matches = [path for path in self.agent_files() if needle in path.stem.casefold()]
        if not matches:
            raise KeyError(f"No agency agent matches: {query}")
        return matches[0]

    def load_agent(self, query: str) -> str:
        return self.find_agent(query).read_text(encoding="utf-8")

    def report(self, *, probe_services: bool = False) -> IntegrationReport:
        count = len(self.agent_files())
        operational = count > 0
        detail = f"{count} agent definition(s) available." if operational else "Agent catalog is not available locally."
        return IntegrationReport(self.phase, self.name, self.mode, self.installed, operational, detail)


class ArtemisAdapter(IntegrationAdapter):
    phase = 7
    name = "artemis"
    mode = "android-cli-mcp"

    def report(self, *, probe_services: bool = False) -> IntegrationReport:
        uv = shutil.which("uv")
        project_ready = (self.repo_path / "pyproject.toml").is_file()
        operational = self.installed and project_ready and uv is not None
        if operational:
            detail = "Artemis runtime is ready; an Android device/emulator is still required for execution."
        elif self.installed and uv is None:
            detail = "Repository cloned, but uv is not installed."
        elif self.installed:
            detail = "Repository cloned, but Artemis project metadata was not found."
        else:
            detail = "Not bootstrapped yet."
        return IntegrationReport(self.phase, self.name, self.mode, self.installed, operational, detail)

    def build_run_command(self, task: str, profile: str = "flash") -> tuple[str, ...]:
        if not task.strip():
            raise ValueError("task cannot be empty")
        if profile not in {"flash", "pro"}:
            raise ValueError("profile must be 'flash' or 'pro'")
        return ("uv", "run", "artemis", "run", task, "--profile", profile)

    def run(
        self,
        task: str,
        *,
        profile: str = "flash",
        dry_run: bool = False,
    ) -> subprocess.CompletedProcess[str] | tuple[str, ...]:
        command = self.build_run_command(task, profile)
        if dry_run:
            return command
        if not self.repo_path.is_dir():
            raise RuntimeError("Artemis repository is not bootstrapped")
        if shutil.which("uv") is None:
            raise RuntimeError("uv is required to run Artemis")
        return subprocess.run(command, cwd=self.repo_path, check=True, capture_output=True, text=True)


ADAPTER_TYPES = (
    GraphifyAdapter,
    ComfyUIAdapter,
    SpecKitAdapter,
    QASkillsAdapter,
    ADHDOutputAdapter,
    AgencyAgentsAdapter,
    ArtemisAdapter,
)


class IntegrationHub:
    def __init__(self, external_root: str | Path = "external", *, comfyui_url: str | None = None) -> None:
        self.external_root = Path(external_root).expanduser().resolve()
        self._adapters: dict[str, IntegrationAdapter] = {}
        for adapter_type in ADAPTER_TYPES:
            if adapter_type is ComfyUIAdapter:
                adapter = adapter_type(self.external_root, endpoint=comfyui_url)
            else:
                adapter = adapter_type(self.external_root)
            self._adapters[adapter.name] = adapter

    def names(self) -> tuple[str, ...]:
        return tuple(adapter.name for adapter in sorted(self._adapters.values(), key=lambda item: item.phase))

    def adapter(self, name: str) -> IntegrationAdapter:
        try:
            return self._adapters[name]
        except KeyError as exc:
            raise KeyError(f"Unknown integration: {name}") from exc

    def reports(self, *, probe_services: bool = False) -> tuple[IntegrationReport, ...]:
        return tuple(
            adapter.report(probe_services=probe_services)
            for adapter in sorted(self._adapters.values(), key=lambda item: item.phase)
        )

    def operational_count(self, *, probe_services: bool = False) -> int:
        return sum(report.operational for report in self.reports(probe_services=probe_services))
