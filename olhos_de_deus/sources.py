from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True, slots=True)
class SourceSpec:
    name: str
    repo: str
    ref: str
    license: str
    role: str

    @property
    def clone_url(self) -> str:
        return f"https://github.com/{self.repo}.git"

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_sources(path: str | Path | None = None) -> tuple[SourceSpec, ...]:
    manifest = Path(path) if path is not None else project_root() / "sources" / "repos.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    raw_sources = data.get("sources")
    if not isinstance(raw_sources, list):
        raise ValueError("sources/repos.json must contain a 'sources' list")

    required = {"name", "repo", "ref", "license", "role"}
    result: list[SourceSpec] = []
    seen: set[str] = set()
    for index, item in enumerate(raw_sources):
        if not isinstance(item, dict) or not required.issubset(item):
            missing = required - set(item) if isinstance(item, dict) else required
            raise ValueError(f"Invalid source at index {index}; missing: {sorted(missing)}")
        name = str(item["name"]).strip()
        if not name or name in seen:
            raise ValueError(f"Duplicate or empty source name: {name!r}")
        seen.add(name)
        result.append(SourceSpec(**{key: str(item[key]) for key in required}))
    return tuple(result)


def select_sources(names: Iterable[str] | None = None) -> tuple[SourceSpec, ...]:
    sources = load_sources()
    if not names:
        return sources
    wanted = {name.strip() for name in names if name.strip()}
    selected = tuple(source for source in sources if source.name in wanted)
    missing = wanted - {source.name for source in selected}
    if missing:
        raise KeyError(f"Unknown source(s): {', '.join(sorted(missing))}")
    return selected
