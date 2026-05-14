from qr_app.history import HistoryEntry
from qr_app.history_filters import (
    HistoryQuery,
    format_history_entries,
    group_history_by_day,
    remove_duplicate_history,
    search_history,
    sort_history,
)


def sample_entries() -> list[HistoryEntry]:
    return [
        HistoryEntry(data="telegram link", output_path="output/telegram.png", created_at="2026-05-13 10:00"),
        HistoryEntry(data="website link", output_path="output/site.png", created_at="2026-05-13 11:00"),
        HistoryEntry(data="telegram link", output_path="output/telegram.png", created_at="2026-05-13 10:00"),
    ]


def test_search_history_filters_by_text() -> None:
    results = search_history(HistoryQuery(text="telegram"), sample_entries())

    assert len(results) == 2


def test_search_history_filters_by_output_and_limit() -> None:
    results = search_history(HistoryQuery(output_contains="site", limit=1), sample_entries())

    assert len(results) == 1
    assert results[0].output_path.endswith("site.png")


def test_sort_history_orders_newest_first() -> None:
    results = sort_history(sample_entries())

    assert results[0].created_at == "2026-05-13 11:00"


def test_remove_duplicate_history_keeps_unique_pairs() -> None:
    assert len(remove_duplicate_history(sample_entries())) == 2


def test_group_history_by_day_groups_entries() -> None:
    groups = group_history_by_day(sample_entries())

    assert list(groups) == ["2026-05-13"]


def test_format_history_entries_handles_empty_list() -> None:
    assert format_history_entries([]) == "No history entries found."
