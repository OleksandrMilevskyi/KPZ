from pathlib import Path

import pytest

from qr_app.batch import generate_batch, parse_batch_csv, parse_batch_file, parse_batch_lines, summarize_batch_results
from qr_app.models import BatchItem


def test_parse_batch_lines_ignores_blank_lines_and_comments(tmp_path: Path) -> None:
    batch_file = tmp_path / "items.txt"
    batch_file.write_text("\n# comment\nfirst\n\nsecond\n", encoding="utf-8")

    items = parse_batch_lines(batch_file)

    assert items == [BatchItem(data="first"), BatchItem(data="second")]


def test_parse_batch_csv_reads_data_and_output_name(tmp_path: Path) -> None:
    batch_file = tmp_path / "items.csv"
    batch_file.write_text("data,output_name\nhello,hello.png\nsite,site\n", encoding="utf-8")

    items = parse_batch_csv(batch_file)

    assert items == [BatchItem(data="hello", output_name="hello.png"), BatchItem(data="site", output_name="site")]


def test_parse_batch_file_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="does not exist"):
        parse_batch_file(tmp_path / "missing.txt")


def test_generate_batch_creates_all_png_files(tmp_path: Path) -> None:
    output_dir = tmp_path / "batch"
    items = [BatchItem(data="first"), BatchItem(data="second", output_name="second-custom.png")]

    results = generate_batch(items, output_dir, save_history=False)

    assert all(result.success for result in results)
    assert len(list(output_dir.glob("*.png"))) == 2


def test_summarize_batch_results_contains_counts(tmp_path: Path) -> None:
    results = generate_batch([BatchItem(data="first")], tmp_path, save_history=False)

    summary = summarize_batch_results(results)

    assert "1 succeeded" in summary
    assert "[OK]" in summary
