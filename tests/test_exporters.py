from datetime import datetime
from pathlib import Path

import pytest

from qr_app.exporters import export_history, normalize_export_format
from qr_app.history import add_history_entry


def test_normalize_export_format_uses_output_suffix() -> None:
    assert normalize_export_format(Path("history.csv"), None) == "csv"
    assert normalize_export_format(Path("history.md"), "markdown") == "md"


def test_normalize_export_format_rejects_unknown_format() -> None:
    with pytest.raises(ValueError, match="Export format"):
        normalize_export_format(Path("history.txt"), None)


def test_export_history_writes_csv(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    history_path = tmp_path / "history.json"
    output_path = tmp_path / "history.csv"
    monkeypatch.setattr("qr_app.exporters.load_history", lambda: add_history_entry(
        "hello",
        tmp_path / "hello.png",
        history_path,
        datetime(2026, 5, 13, 10, 0),
    ))

    result = export_history(output_path)

    assert result.item_count == 1
    assert "hello" in output_path.read_text(encoding="utf-8")


def test_export_history_writes_markdown(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    history_path = tmp_path / "history.json"
    output_path = tmp_path / "history.md"
    monkeypatch.setattr("qr_app.exporters.load_history", lambda: add_history_entry(
        "hello | world",
        tmp_path / "hello.png",
        history_path,
        datetime(2026, 5, 13, 10, 0),
    ))

    export_history(output_path)

    assert "\\|" in output_path.read_text(encoding="utf-8")
