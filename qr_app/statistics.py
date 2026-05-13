from __future__ import annotations

from collections import Counter
from pathlib import Path

from .history import HistoryEntry, load_history
from .models import HistoryStats


def calculate_history_stats(entries: list[HistoryEntry] | None = None) -> HistoryStats:
    entries = entries if entries is not None else load_history()
    if not entries:
        return HistoryStats(
            total_items=0,
            unique_outputs=0,
            first_created_at=None,
            last_created_at=None,
            longest_data=None,
        )

    unique_outputs = len({entry.output_path for entry in entries})
    sorted_entries = sorted(entries, key=lambda entry: entry.created_at)
    longest_data = max(entries, key=lambda entry: len(entry.data)).data

    return HistoryStats(
        total_items=len(entries),
        unique_outputs=unique_outputs,
        first_created_at=sorted_entries[0].created_at,
        last_created_at=sorted_entries[-1].created_at,
        longest_data=longest_data,
    )


def count_outputs_by_folder(entries: list[HistoryEntry] | None = None) -> dict[str, int]:
    entries = entries if entries is not None else load_history()
    counter: Counter[str] = Counter()
    for entry in entries:
        folder = str(Path(entry.output_path).parent)
        counter[folder] += 1
    return dict(counter)


def format_history_stats(stats: HistoryStats) -> str:
    if stats.total_items == 0:
        return "History is empty."

    lines = [
        f"Total generated QR codes: {stats.total_items}",
        f"Unique output files: {stats.unique_outputs}",
        f"First generation: {stats.first_created_at}",
        f"Latest generation: {stats.last_created_at}",
        f"Longest stored data: {stats.longest_data}",
    ]
    return "\n".join(lines)
