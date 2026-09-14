from pathlib import Path

from olhos_de_deus.desktop import AppPaths, DesktopController, DesktopStorage


def test_app_paths_create_windows_style_data_tree(tmp_path):
    paths = AppPaths.from_root(tmp_path / "OlhosDeDeus").ensure()
    assert paths.root.is_dir()
    assert paths.database.parent.is_dir()
    assert paths.logs.is_dir()
    assert paths.config.is_dir()
    assert paths.cache.is_dir()
    assert paths.missions.is_dir()
    assert paths.external.is_dir()


def test_desktop_storage_round_trips_settings_missions_and_logs(tmp_path):
    storage = DesktopStorage(tmp_path / "database" / "app.db")
    storage.set_setting("comfyui_url", "http://127.0.0.1:8188")
    assert storage.get_setting("comfyui_url") == "http://127.0.0.1:8188"

    storage.start_mission("abc123", "Test mission")
    storage.log("TEST", "started", mission_id="abc123", phase="test")
    storage.finish_mission(
        "abc123",
        status="verified",
        duration_ms=42,
        result={"ok": True},
    )

    mission = storage.recent_missions(1)[0]
    assert mission["id"] == "abc123"
    assert mission["status"] == "verified"
    assert mission["result"] == {"ok": True}
    assert storage.recent_logs(1)[0]["message"] == "started"


def test_desktop_controller_reports_seven_integrations(tmp_path):
    paths = AppPaths.from_root(tmp_path / "data")
    controller = DesktopController(paths=paths)
    dashboard = controller.dashboard()
    assert dashboard["total_integrations"] == 7
    assert dashboard["summary"]["missions"] == 0
    assert Path(dashboard["external_root"]).is_dir()


def test_desktop_controller_runs_and_persists_mission(tmp_path):
    controller = DesktopController(paths=AppPaths.from_root(tmp_path / "data"))
    result = controller.run_mission("Corrigir bug no projeto")
    assert result["mission"]["status"] == "verified"
    assert result["duration_ms"] >= 0
    recent = controller.storage.recent_missions(1)[0]
    assert recent["status"] == "verified"
    assert recent["request"] == "Corrigir bug no projeto"


def test_desktop_phase_preview_is_safe_dry_run(tmp_path):
    controller = DesktopController(paths=AppPaths.from_root(tmp_path / "data"))
    result = controller.phase_preview("graphify", target=".")
    assert result["phase"] == 1
    assert result["execute"] is False
    assert result["command"] == ["graphify", "."]
