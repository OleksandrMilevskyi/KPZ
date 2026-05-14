from pathlib import Path

from qr_app.reports import build_files_table, build_history_table, build_project_report


def test_build_history_table_handles_empty_history() -> None:
    assert "No history" in build_history_table([])


def test_build_files_table_handles_empty_files() -> None:
    assert "No generated" in build_files_table([])


def test_build_project_report_creates_html_file(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    output_path = tmp_path / "report.html"

    result = build_project_report(output_path)

    assert result == output_path.resolve()
    assert "<html" in output_path.read_text(encoding="utf-8")
