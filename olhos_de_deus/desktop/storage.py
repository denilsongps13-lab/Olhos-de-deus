from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterator


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


class DesktopStorage:
    """Small SQLite store for missions, logs and non-sensitive settings."""

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path).expanduser().resolve()
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path, timeout=10)
        connection.row_factory = sqlite3.Row
        try:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("PRAGMA journal_mode = WAL")
            yield connection
            connection.commit()
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self._connect() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS missions (
                    id TEXT PRIMARY KEY,
                    request TEXT NOT NULL,
                    status TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    finished_at TEXT,
                    duration_ms INTEGER,
                    result_json TEXT,
                    error TEXT
                );

                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    level TEXT NOT NULL,
                    source TEXT NOT NULL,
                    message TEXT NOT NULL,
                    mission_id TEXT,
                    phase TEXT,
                    payload_json TEXT,
                    FOREIGN KEY(mission_id) REFERENCES missions(id)
                );

                CREATE INDEX IF NOT EXISTS idx_logs_created_at ON logs(created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_logs_mission_id ON logs(mission_id);

                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                """
            )

    def set_setting(self, key: str, value: Any) -> None:
        if not key.strip():
            raise ValueError("setting key cannot be empty")
        with self._connect() as db:
            db.execute(
                """
                INSERT INTO settings(key, value_json, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    value_json=excluded.value_json,
                    updated_at=excluded.updated_at
                """,
                (key, json.dumps(value, ensure_ascii=False), _utc_now()),
            )

    def get_setting(self, key: str, default: Any = None) -> Any:
        with self._connect() as db:
            row = db.execute("SELECT value_json FROM settings WHERE key = ?", (key,)).fetchone()
        if row is None:
            return default
        return json.loads(row["value_json"])

    def all_settings(self) -> dict[str, Any]:
        with self._connect() as db:
            rows = db.execute("SELECT key, value_json FROM settings ORDER BY key").fetchall()
        return {row["key"]: json.loads(row["value_json"]) for row in rows}

    def start_mission(self, mission_id: str, request: str) -> str:
        started_at = _utc_now()
        with self._connect() as db:
            db.execute(
                "INSERT INTO missions(id, request, status, started_at) VALUES (?, ?, ?, ?)",
                (mission_id, request, "running", started_at),
            )
        return started_at

    def finish_mission(
        self,
        mission_id: str,
        *,
        status: str,
        duration_ms: int,
        result: Any | None = None,
        error: str | None = None,
    ) -> None:
        with self._connect() as db:
            db.execute(
                """
                UPDATE missions
                SET status = ?, finished_at = ?, duration_ms = ?, result_json = ?, error = ?
                WHERE id = ?
                """,
                (
                    status,
                    _utc_now(),
                    int(duration_ms),
                    None if result is None else json.dumps(result, ensure_ascii=False),
                    error,
                    mission_id,
                ),
            )

    def log(
        self,
        source: str,
        message: str,
        *,
        level: str = "INFO",
        mission_id: str | None = None,
        phase: str | None = None,
        payload: Any | None = None,
    ) -> None:
        safe_payload = None if payload is None else json.dumps(payload, ensure_ascii=False)
        with self._connect() as db:
            db.execute(
                """
                INSERT INTO logs(created_at, level, source, message, mission_id, phase, payload_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (_utc_now(), level.upper(), source, message, mission_id, phase, safe_payload),
            )

    def recent_missions(self, limit: int = 20) -> list[dict[str, Any]]:
        with self._connect() as db:
            rows = db.execute(
                """
                SELECT id, request, status, started_at, finished_at, duration_ms, result_json, error
                FROM missions ORDER BY started_at DESC LIMIT ?
                """,
                (max(1, int(limit)),),
            ).fetchall()
        result: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            raw_result = item.pop("result_json")
            item["result"] = json.loads(raw_result) if raw_result else None
            result.append(item)
        return result

    def recent_logs(self, limit: int = 300) -> list[dict[str, Any]]:
        with self._connect() as db:
            rows = db.execute(
                """
                SELECT id, created_at, level, source, message, mission_id, phase, payload_json
                FROM logs ORDER BY id DESC LIMIT ?
                """,
                (max(1, int(limit)),),
            ).fetchall()
        result: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            raw_payload = item.pop("payload_json")
            item["payload"] = json.loads(raw_payload) if raw_payload else None
            result.append(item)
        return result

    def summary(self) -> dict[str, int]:
        with self._connect() as db:
            missions = db.execute("SELECT COUNT(*) AS count FROM missions").fetchone()["count"]
            failures = db.execute("SELECT COUNT(*) AS count FROM missions WHERE status = 'failed'").fetchone()["count"]
            logs = db.execute("SELECT COUNT(*) AS count FROM logs").fetchone()["count"]
        return {"missions": int(missions), "failures": int(failures), "logs": int(logs)}
