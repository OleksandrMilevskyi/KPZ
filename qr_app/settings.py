from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


DEFAULT_SETTINGS_PATH = Path("output/settings.json")


@dataclass(frozen=True)
class AppSettings:
    default_output_dir: str = "output"
    default_history_export: str = "output/history.md"
    remember_history: bool = True
    overwrite_files: bool = True
    validate_urls: bool = False
    active_profile: str = "classic"


def load_settings(path: Path = DEFAULT_SETTINGS_PATH) -> AppSettings:
    if not path.exists():
        return AppSettings()

    try:
        raw_settings = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return AppSettings()

    return parse_settings(raw_settings)


def save_settings(settings: AppSettings, path: Path = DEFAULT_SETTINGS_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(settings), indent=2), encoding="utf-8")


def parse_settings(raw_settings: Any) -> AppSettings:
    if not isinstance(raw_settings, dict):
        return AppSettings()

    return AppSettings(
        default_output_dir=str(raw_settings.get("default_output_dir", "output")),
        default_history_export=str(raw_settings.get("default_history_export", "output/history.md")),
        remember_history=parse_bool_setting(raw_settings.get("remember_history", True)),
        overwrite_files=parse_bool_setting(raw_settings.get("overwrite_files", True)),
        validate_urls=parse_bool_setting(raw_settings.get("validate_urls", False)),
        active_profile=str(raw_settings.get("active_profile", "classic")),
    )


def update_settings(path: Path = DEFAULT_SETTINGS_PATH, **updates: object) -> AppSettings:
    current = load_settings(path)
    allowed_keys = set(AppSettings.__dataclass_fields__)
    clean_updates = {key: value for key, value in updates.items() if key in allowed_keys and value is not None}
    next_settings = AppSettings(**{**asdict(current), **clean_updates})
    save_settings(next_settings, path)
    return next_settings


def parse_bool_setting(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return bool(value)


def format_settings(settings: AppSettings) -> str:
    lines = ["Application settings:"]
    for key, value in asdict(settings).items():
        lines.append(f"- {key}: {value}")
    return "\n".join(lines)
