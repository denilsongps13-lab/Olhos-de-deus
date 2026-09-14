from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

APP_DIR_NAME = "OlhosDeDeus"


def _default_root() -> Path:
    if os.name == "nt":
        base = os.getenv("LOCALAPPDATA")
        if base:
            return Path(base) / APP_DIR_NAME
        return Path.home() / "AppData" / "Local" / APP_DIR_NAME
    xdg = os.getenv("XDG_DATA_HOME")
    if xdg:
        return Path(xdg) / APP_DIR_NAME
    return Path.home() / ".local" / "share" / APP_DIR_NAME


@dataclass(frozen=True, slots=True)
class AppPaths:
    root: Path
    database: Path
    logs: Path
    config: Path
    cache: Path
    missions: Path
    external: Path

    @classmethod
    def from_root(cls, root: str | Path) -> "AppPaths":
        base = Path(root).expanduser().resolve()
        return cls(
            root=base,
            database=base / "database" / "olhos_de_deus.db",
            logs=base / "logs",
            config=base / "config",
            cache=base / "cache",
            missions=base / "missions",
            external=base / "external",
        )

    @classmethod
    def default(cls) -> "AppPaths":
        override = os.getenv("OLHOS_DE_DEUS_DATA_DIR")
        return cls.from_root(override or _default_root())

    def ensure(self) -> "AppPaths":
        self.root.mkdir(parents=True, exist_ok=True)
        self.database.parent.mkdir(parents=True, exist_ok=True)
        self.logs.mkdir(parents=True, exist_ok=True)
        self.config.mkdir(parents=True, exist_ok=True)
        self.cache.mkdir(parents=True, exist_ok=True)
        self.missions.mkdir(parents=True, exist_ok=True)
        self.external.mkdir(parents=True, exist_ok=True)
        return self
