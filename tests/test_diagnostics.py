from pathlib import Path

from qr_app.diagnostics import (
    DiagnosticCheck,
    check_dependency,
    check_output_directory,
    check_project_file,
    diagnostics_passed,
    format_diagnostics,
    run_diagnostics,
)


def test_check_dependency_detects_known_module() -> None:
    assert check_dependency("json").passed is True


def test_check_project_file_reports_existing_file(tmp_path: Path) -> None:
    path = tmp_path / "file.txt"
    path.write_text("ok", encoding="utf-8")

    assert check_project_file(path).passed is True


def test_check_output_directory_creates_directory(tmp_path: Path) -> None:
    output_dir = tmp_path / "output"

    assert check_output_directory(output_dir).passed is True
    assert output_dir.exists()


def test_format_diagnostics_contains_status() -> None:
    text = format_diagnostics([DiagnosticCheck("Test", True, "message")])

    assert "[OK] Test" in text


def test_diagnostics_passed_requires_all_checks_to_pass() -> None:
    assert diagnostics_passed([DiagnosticCheck("A", True, ""), DiagnosticCheck("B", False, "")]) is False


def test_run_diagnostics_returns_checks(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("readme", encoding="utf-8")
    (tmp_path / "requirements.txt").write_text("requirements", encoding="utf-8")

    assert run_diagnostics(tmp_path)
