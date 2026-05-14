from pathlib import Path

import pytest

from qr_app.backup import create_backup, format_backup_result, list_backup_contents, restore_backup


def test_create_backup_archives_known_files(tmp_path: Path) -> None:
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    (output_dir / "history.json").write_text("[]", encoding="utf-8")
    (output_dir / "ignored.txt").write_text("ignored", encoding="utf-8")
    archive_path = tmp_path / "backup.zip"

    result = create_backup(output_dir, archive_path)

    assert result.file_count == 1
    assert list_backup_contents(archive_path) == ["history.json"]


def test_restore_backup_restores_known_files(tmp_path: Path) -> None:
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    (output_dir / "settings.json").write_text("{}", encoding="utf-8")
    archive_path = tmp_path / "backup.zip"
    create_backup(output_dir, archive_path)
    (output_dir / "settings.json").unlink()

    result = restore_backup(archive_path, output_dir)

    assert result.file_count == 1
    assert (output_dir / "settings.json").exists()


def test_list_backup_contents_rejects_missing_archive(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="does not exist"):
        list_backup_contents(tmp_path / "missing.zip")


def test_format_backup_result_contains_action(tmp_path: Path) -> None:
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    result = create_backup(output_dir, tmp_path / "backup.zip")

    assert "Backup created" in format_backup_result(result, "Backup created")
