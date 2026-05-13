from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_HISTORY_PATH = Path("output/history.json")
MAX_HISTORY_ITEMS = 10


@dataclass(frozen=True)
class HistoryEntry:
    data: str
    output_path: str
    created_at: str


def load_history(history_path: Path = DEFAULT_HISTORY_PATH) -> list[HistoryEntry]:
    if not history_path.exists():
        return []

    try:
        raw_items = json.loads(history_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    if not isinstance(raw_items, list):
        return []

    entries: list[HistoryEntry] = []
    for item in raw_items:
        entry = _parse_history_item(item)
        if entry is not None:
            entries.append(entry)
    return entries


def save_history(entries: list[HistoryEntry], history_path: Path = DEFAULT_HISTORY_PATH) -> None:
    history_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(entry) for entry in entries[:MAX_HISTORY_ITEMS]]
    history_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def add_history_entry(
    data: str,
    output_path: Path,
    history_path: Path = DEFAULT_HISTORY_PATH,
    created_at: datetime | None = None,
) -> list[HistoryEntry]:
    timestamp = (created_at or datetime.now()).strftime("%Y-%m-%d %H:%M")
    entry = HistoryEntry(
        data=_shorten_data(data.strip()),
        output_path=str(output_path.resolve()),
        created_at=timestamp,
    )
    entries = [entry, *load_history(history_path)]
    save_history(entries, history_path)
    return entries[:MAX_HISTORY_ITEMS]


def _parse_history_item(item: Any) -> HistoryEntry | None:
    if not isinstance(item, dict):
        return None

    data = item.get("data")
    output_path = item.get("output_path")
    created_at = item.get("created_at")
    if not all(isinstance(value, str) for value in (data, output_path, created_at)):
        return None

    return HistoryEntry(data=data, output_path=output_path, created_at=created_at)


def _shorten_data(data: str, limit: int = 80) -> str:
    if len(data) <= limit:
        return data
    return f"{data[: limit - 3]}..."
