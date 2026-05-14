from __future__ import annotations

from dataclasses import dataclass

from .history import HistoryEntry, load_history


@dataclass(frozen=True)
class HistoryQuery:
    text: str = ""
    output_contains: str = ""
    created_from: str = ""
    created_to: str = ""
    limit: int = 0


def search_history(query: HistoryQuery, entries: list[HistoryEntry] | None = None) -> list[HistoryEntry]:
    entries = entries if entries is not None else load_history()
    results = entries

    if query.text:
        needle = query.text.lower()
        results = [entry for entry in results if needle in entry.data.lower()]

    if query.output_contains:
        output_needle = query.output_contains.lower()
        results = [entry for entry in results if output_needle in entry.output_path.lower()]

    if query.created_from:
        results = [entry for entry in results if entry.created_at >= query.created_from]

    if query.created_to:
        results = [entry for entry in results if entry.created_at <= query.created_to]

    results = sort_history(results)
    if query.limit > 0:
        return results[: query.limit]
    return results


def sort_history(entries: list[HistoryEntry], newest_first: bool = True) -> list[HistoryEntry]:
    return sorted(entries, key=lambda entry: entry.created_at, reverse=newest_first)


def remove_duplicate_history(entries: list[HistoryEntry]) -> list[HistoryEntry]:
    seen: set[tuple[str, str]] = set()
    unique_entries: list[HistoryEntry] = []
    for entry in entries:
        key = (entry.data, entry.output_path)
        if key in seen:
            continue
        seen.add(key)
        unique_entries.append(entry)
    return unique_entries


def group_history_by_day(entries: list[HistoryEntry]) -> dict[str, list[HistoryEntry]]:
    groups: dict[str, list[HistoryEntry]] = {}
    for entry in entries:
        day = entry.created_at[:10] if len(entry.created_at) >= 10 else "unknown"
        groups.setdefault(day, []).append(entry)
    return groups


def format_history_entries(entries: list[HistoryEntry]) -> str:
    if not entries:
        return "No history entries found."

    lines = []
    for entry in entries:
        lines.append(f"{entry.created_at} | {entry.data} | {entry.output_path}")
    return "\n".join(lines)
