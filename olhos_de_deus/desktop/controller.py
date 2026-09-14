from __future__ import annotations

import json
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable
from uuid import uuid4

from olhos_de_deus import __version__
from olhos_de_deus.bootstrap import bootstrap_sources
from olhos_de_deus.integrations import IntegrationHub
from olhos_de_deus.orchestrator import Orchestrator

from .paths import AppPaths
from .storage import DesktopStorage


class DesktopController:
    """UI-facing facade. It keeps Qt code away from core execution logic."""

    def __init__(
        self,
        *,
        paths: AppPaths | None = None,
        storage: DesktopStorage | None = None,
        orchestrator: Orchestrator | None = None,
    ) -> None:
        self.paths = (paths or AppPaths.default()).ensure()
        self.storage = storage or DesktopStorage(self.paths.database)
        self.orchestrator = orchestrator or Orchestrator()

        if self.storage.get_setting("external_root") is None:
            self.storage.set_setting("external_root", str(self.paths.external))
        if self.storage.get_setting("comfyui_url") is None:
            self.storage.set_setting("comfyui_url", "http://127.0.0.1:8188")
        if self.storage.get_setting("dry_run_default") is None:
            self.storage.set_setting("dry_run_default", True)

    @property
    def external_root(self) -> Path:
        return Path(self.storage.get_setting("external_root", str(self.paths.external))).expanduser().resolve()

    @property
    def comfyui_url(self) -> str:
        return str(self.storage.get_setting("comfyui_url", "http://127.0.0.1:8188"))

    def integration_hub(self) -> IntegrationHub:
        return IntegrationHub(self.external_root, comfyui_url=self.comfyui_url)

    def dashboard(self) -> dict[str, Any]:
        reports = self.integration_hub().reports(probe_services=False)
        recent = self.storage.recent_missions(1)
        summary = self.storage.summary()
        return {
            "version": __version__,
            "operational": sum(item.operational for item in reports),
            "installed": sum(item.installed for item in reports),
            "total_integrations": len(reports),
            "integrations": [item.to_dict() for item in reports],
            "last_mission": recent[0] if recent else None,
            "summary": summary,
            "data_root": str(self.paths.root),
            "external_root": str(self.external_root),
            "comfyui_url": self.comfyui_url,
        }

    def doctor(self, *, probe_services: bool = False) -> list[dict[str, Any]]:
        self.storage.log("SYSTEM_DOCTOR", "Diagnostic started", payload={"probe_services": probe_services})
        reports = self.integration_hub().reports(probe_services=probe_services)
        payload = [item.to_dict() for item in reports]
        self.storage.log(
            "SYSTEM_DOCTOR",
            "Diagnostic completed",
            payload={"operational": sum(item.operational for item in reports), "total": len(reports)},
        )
        return payload

    def run_mission(self, request: str) -> dict[str, Any]:
        text = request.strip()
        if not text:
            raise ValueError("mission request cannot be empty")

        execution_id = uuid4().hex[:12]
        self.storage.start_mission(execution_id, text)
        self.storage.log("ORCHESTRATOR", "Mission received", mission_id=execution_id, payload={"request": text})
        started = time.perf_counter()
        try:
            mission = self.orchestrator.run(text)
            duration_ms = int((time.perf_counter() - started) * 1000)
            result = asdict(mission)
            status = str(mission.status)
            self.storage.finish_mission(
                execution_id,
                status=status,
                duration_ms=duration_ms,
                result=result,
                error=None,
            )
            for step in result.get("steps", []):
                self.storage.log(
                    "MISSION",
                    f"{step['name']}: {step['status']}",
                    mission_id=execution_id,
                    phase=step.get("capability"),
                    payload={"evidence": step.get("evidence", []), "error": step.get("error")},
                )
            self.storage.log(
                "ORCHESTRATOR",
                f"Mission finished: {status}",
                mission_id=execution_id,
                payload={"duration_ms": duration_ms, "core_mission_id": mission.id},
            )
            return {
                "execution_id": execution_id,
                "duration_ms": duration_ms,
                "mission": result,
            }
        except Exception as exc:
            duration_ms = int((time.perf_counter() - started) * 1000)
            self.storage.finish_mission(
                execution_id,
                status="failed",
                duration_ms=duration_ms,
                error=str(exc),
            )
            self.storage.log(
                "ORCHESTRATOR",
                str(exc),
                level="ERROR",
                mission_id=execution_id,
                payload={"duration_ms": duration_ms},
            )
            raise

    def bootstrap(
        self,
        names: Iterable[str] | None = None,
        *,
        dry_run: bool = True,
    ) -> list[dict[str, Any]]:
        self.external_root.mkdir(parents=True, exist_ok=True)
        results = bootstrap_sources(self.external_root, names, dry_run=dry_run)
        payload = [asdict(item) for item in results]
        self.storage.log(
            "BOOTSTRAP",
            "Bootstrap planned" if dry_run else "Bootstrap completed",
            payload={"dry_run": dry_run, "sources": [item["source"] for item in payload]},
        )
        return payload

    def phase_preview(self, name: str, **kwargs: Any) -> dict[str, Any]:
        hub = self.integration_hub()
        adapter = hub.adapter(name)

        if name == "graphify":
            target = kwargs.get("target", ".")
            return {"phase": 1, "name": name, "execute": False, "command": adapter.run(target, dry_run=True)}
        if name == "comfyui":
            return adapter.report(probe_services=bool(kwargs.get("probe", False))).to_dict()
        if name == "spec-kit":
            target = kwargs.get("target", ".")
            integration = kwargs.get("integration", "copilot")
            return {
                "phase": 3,
                "name": name,
                "execute": False,
                "target": str(Path(target).expanduser().resolve()),
                "command": adapter.init_project(target, integration=integration, dry_run=True),
            }
        if name == "qa-skills":
            return {"phase": 4, "name": name, "skills": adapter.list_skills()}
        if name == "i-have-adhd":
            return {"phase": 5, "name": name, "rules": adapter.load_rules()}
        if name == "agency-agents":
            query = str(kwargs.get("query", "")).strip()
            if query:
                path = adapter.find_agent(query)
                return {"phase": 6, "name": name, "agent": path.stem, "path": str(path)}
            return {"phase": 6, "name": name, "agents": adapter.list_agents()}
        if name == "artemis":
            task = str(kwargs.get("task", "Open Settings"))
            profile = str(kwargs.get("profile", "flash"))
            return {"phase": 7, "name": name, "execute": False, "command": adapter.run(task, profile=profile, dry_run=True)}
        raise KeyError(f"Unknown integration: {name}")

    def queue_comfyui_workflow(self, workflow_path: str | Path) -> Any:
        path = Path(workflow_path).expanduser().resolve()
        workflow = json.loads(path.read_text(encoding="utf-8"))
        result = self.integration_hub().adapter("comfyui").queue_prompt(workflow)
        self.storage.log("COMFYUI", "Workflow queued", phase="comfyui", payload={"workflow": str(path)})
        return result

    def save_settings(
        self,
        *,
        external_root: str | Path | None = None,
        comfyui_url: str | None = None,
        dry_run_default: bool | None = None,
    ) -> dict[str, Any]:
        if external_root is not None:
            path = Path(external_root).expanduser().resolve()
            path.mkdir(parents=True, exist_ok=True)
            self.storage.set_setting("external_root", str(path))
        if comfyui_url is not None:
            url = comfyui_url.strip().rstrip("/")
            if not (url.startswith("http://") or url.startswith("https://")):
                raise ValueError("ComfyUI URL must start with http:// or https://")
            self.storage.set_setting("comfyui_url", url)
        if dry_run_default is not None:
            self.storage.set_setting("dry_run_default", bool(dry_run_default))
        self.storage.log("SETTINGS", "Settings updated")
        return self.storage.all_settings()
