from pathlib import Path

import pytest

from qr_app.file_manager import (
    calculate_output_size,
    delete_output_files,
    find_old_output_files,
    format_file_size,
    list_output_files,
    summarize_output_folder,
)


def test_list_output_files_returns_png_files_newest_first(tmp_path: Path) -> None:
    first = tmp_path / "first.png"
    second = tmp_path / "second.png"
    first.write_bytes(b"1")
    second.write_bytes(b"22")

    files = list_output_files(tmp_path)

    assert {file_info.path.name for file_info in files} == {"first.png", "second.png"}


def test_calculate_output_size_sums_png_files(tmp_path: Path) -> None:
    (tmp_path / "a.png").write_bytes(b"123")
    (tmp_path / "b.txt").write_bytes(b"ignored")

    assert calculate_output_size(tmp_path) == 3


def test_find_old_output_files_validates_keep_latest(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        find_old_output_files(tmp_path, -1)


def test_delete_output_files_removes_files(tmp_path: Path) -> None:
    path = tmp_path / "a.png"
    path.write_bytes(b"123")
    files = list_output_files(tmp_path)

    assert delete_output_files(files) == 1
    assert not path.exists()


def test_format_file_size_uses_readable_units() -> None:
    assert format_file_size(12) == "12 B"
    assert format_file_size(2048) == "2.0 KB"


def test_summarize_output_folder_contains_count(tmp_path: Path) -> None:
    (tmp_path / "a.png").write_bytes(b"123")

    assert "PNG files: 1" in summarize_output_folder(tmp_path)
