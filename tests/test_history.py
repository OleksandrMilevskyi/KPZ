from datetime import datetime
from pathlib import Path

from qr_app.history import MAX_HISTORY_ITEMS, HistoryEntry, add_history_entry, load_history, save_history


def test_add_history_entry_persists_newest_first(tmp_path: Path) -> None:
    history_path = tmp_path / "history.json"
    first_file = tmp_path / "first.png"
    second_file = tmp_path / "second.png"

    add_history_entry("first", first_file, history_path, datetime(2026, 5, 13, 10, 0))
    entries = add_history_entry("second", second_file, history_path, datetime(2026, 5, 13, 10, 30))

    assert [entry.data for entry in entries] == ["second", "first"]
    assert load_history(history_path) == entries


def test_save_history_keeps_recent_limit(tmp_path: Path) -> None:
    history_path = tmp_path / "history.json"
    entries = [
        HistoryEntry(data=f"item {index}", output_path=f"{index}.png", created_at="2026-05-13 10:00")
        for index in range(MAX_HISTORY_ITEMS + 2)
    ]

    save_history(entries, history_path)

    assert len(load_history(history_path)) == MAX_HISTORY_ITEMS


def test_load_history_ignores_broken_file(tmp_path: Path) -> None:
    history_path = tmp_path / "history.json"
    history_path.write_text("not json", encoding="utf-8")

    assert load_history(history_path) == []
