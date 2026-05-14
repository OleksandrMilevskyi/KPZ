from __future__ import annotations

import importlib.util
import platform
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DiagnosticCheck:
    name: str
    passed: bool
    message: str


def run_diagnostics(project_root: Path = Path(".")) -> list[DiagnosticCheck]:
    checks = [
        check_python_version(),
        check_dependency("qrcode"),
        check_dependency("PIL"),
        check_project_file(project_root / "requirements.txt"),
        check_project_file(project_root / "README.md"),
        check_output_directory(project_root / "output"),
    ]
    return checks


def check_python_version() -> DiagnosticCheck:
    version = platform.python_version()
    major, minor, *_ = platform.python_version_tuple()
    passed = int(major) >= 3 and int(minor) >= 10
    return DiagnosticCheck(
        name="Python version",
        passed=passed,
        message=f"Python {version}",
    )


def check_dependency(module_name: str) -> DiagnosticCheck:
    spec = importlib.util.find_spec(module_name)
    return DiagnosticCheck(
        name=f"Dependency {module_name}",
        passed=spec is not None,
        message="installed" if spec is not None else "missing",
    )


def check_project_file(path: Path) -> DiagnosticCheck:
    return DiagnosticCheck(
        name=f"Project file {path.name}",
        passed=path.exists(),
        message=str(path),
    )


def check_output_directory(path: Path) -> DiagnosticCheck:
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".write-test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return DiagnosticCheck(name="Output directory", passed=True, message=str(path.resolve()))
    except OSError as error:
        return DiagnosticCheck(name="Output directory", passed=False, message=str(error))


def format_diagnostics(checks: list[DiagnosticCheck]) -> str:
    lines = ["Diagnostics:"]
    for check in checks:
        status = "OK" if check.passed else "FAIL"
        lines.append(f"[{status}] {check.name}: {check.message}")
    return "\n".join(lines)


def diagnostics_passed(checks: list[DiagnosticCheck]) -> bool:
    return all(check.passed for check in checks)
