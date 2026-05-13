from pathlib import Path

from qr_app.cli import main, normalize_argv


def test_normalize_argv_keeps_known_subcommands() -> None:
    assert normalize_argv(["stats"]) == ["stats"]


def test_normalize_argv_converts_legacy_text_to_single_command() -> None:
    assert normalize_argv(["hello", "--output", "hello.png"]) == ["single", "hello", "--output", "hello.png"]


def test_normalize_argv_keeps_options_without_guessing_command() -> None:
    assert normalize_argv(["--help"]) == ["--help"]


def test_normalize_argv_handles_empty_argument_list() -> None:
    assert normalize_argv([]) == []


def test_normalize_argv_preserves_none_for_runtime_arguments() -> None:
    normalized = normalize_argv(None)
    assert normalized is not None


def test_cli_legacy_single_generation(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = main(["hello", "--output", "hello.png", "--no-history"])

    assert exit_code == 0
    assert (tmp_path / "hello.png").exists()


def test_cli_single_subcommand_generation(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = main(["single", "hello", "--output", "single.png", "--no-history"])

    assert exit_code == 0
    assert (tmp_path / "single.png").exists()


def test_cli_template_generation(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = main(["template", "phone", "phone=+380000000000", "--output", "phone.png", "--no-history"])

    assert exit_code == 0
    assert (tmp_path / "phone.png").exists()


def test_cli_batch_generation(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    batch_file = tmp_path / "batch.txt"
    batch_file.write_text("one\ntwo\n", encoding="utf-8")

    exit_code = main(["batch", str(batch_file), "--output-dir", "batch-output"])

    assert exit_code == 0
    assert len(list((tmp_path / "batch-output").glob("*.png"))) == 2


def test_cli_profiles_command(capsys) -> None:
    exit_code = main(["profiles"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "classic" in captured.out


def test_cli_settings_command(capsys, tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = main(["settings"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Application settings" in captured.out


def test_cli_stats_command(capsys, tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = main(["stats"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "History is empty" in captured.out


def test_cli_export_history_command(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = main(["export-history", "history.md"])

    assert exit_code == 0
    assert (tmp_path / "history.md").exists()


def test_cli_report_command(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = main(["report", "--output", "report.html"])

    assert exit_code == 0
    assert (tmp_path / "report.html").exists()


def test_cli_output_summary_command(capsys, tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = main(["output-summary", "--output-dir", "output"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Output folder" in captured.out


def test_cli_search_history_command(capsys, tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = main(["search-history", "--text", "missing"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "No history entries" in captured.out
