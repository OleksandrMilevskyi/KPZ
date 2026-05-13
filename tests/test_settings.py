from pathlib import Path

from qr_app.settings import AppSettings, format_settings, load_settings, save_settings, update_settings


def test_load_settings_returns_defaults_for_missing_file(tmp_path: Path) -> None:
    assert load_settings(tmp_path / "missing.json") == AppSettings()


def test_save_and_load_settings_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    settings = AppSettings(default_output_dir="custom", remember_history=False)

    save_settings(settings, path)

    assert load_settings(path) == settings


def test_update_settings_changes_known_values(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"

    settings = update_settings(path, default_output_dir="new-output", unknown="ignored")

    assert settings.default_output_dir == "new-output"
    assert load_settings(path).default_output_dir == "new-output"


def test_format_settings_contains_values() -> None:
    text = format_settings(AppSettings(default_output_dir="out"))

    assert "default_output_dir: out" in text
