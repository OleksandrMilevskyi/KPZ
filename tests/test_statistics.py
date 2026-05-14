from qr_app.history import HistoryEntry
from qr_app.statistics import calculate_history_stats, count_outputs_by_folder, format_history_stats


def test_calculate_history_stats_returns_empty_stats() -> None:
    stats = calculate_history_stats([])

    assert stats.total_items == 0
    assert format_history_stats(stats) == "History is empty."


def test_calculate_history_stats_counts_entries() -> None:
    entries = [
        HistoryEntry(data="short", output_path="output/a.png", created_at="2026-05-13 10:00"),
        HistoryEntry(data="longer data", output_path="output/b.png", created_at="2026-05-13 11:00"),
    ]

    stats = calculate_history_stats(entries)

    assert stats.total_items == 2
    assert stats.unique_outputs == 2
    assert stats.longest_data == "longer data"


def test_count_outputs_by_folder_groups_paths() -> None:
    entries = [
        HistoryEntry(data="one", output_path="output/a.png", created_at="2026-05-13 10:00"),
        HistoryEntry(data="two", output_path="output/b.png", created_at="2026-05-13 10:30"),
    ]

    assert count_outputs_by_folder(entries) == {"output": 2}
