from __future__ import annotations

import csv
import html
import json
from pathlib import Path

from .history import HistoryEntry, load_history
from .models import ExportResult


SUPPORTED_EXPORT_FORMATS = {"csv", "json", "md", "html"}


def export_history(output_path: Path, format_name: str | None = None) -> ExportResult:
    entries = load_history()
    clean_format = normalize_export_format(output_path, format_name)

    if clean_format == "csv":
        write_history_csv(entries, output_path)
    elif clean_format == "json":
        write_history_json(entries, output_path)
    elif clean_format == "md":
        write_history_markdown(entries, output_path)
    elif clean_format == "html":
        write_history_html(entries, output_path)
    else:
        raise ValueError(f"Unsupported export format: {clean_format}")

    return ExportResult(output_path=output_path.resolve(), item_count=len(entries), format_name=clean_format)


def normalize_export_format(output_path: Path, format_name: str | None) -> str:
    if format_name:
        clean_format = format_name.strip().lower().lstrip(".")
    else:
        clean_format = output_path.suffix.lower().lstrip(".")

    if clean_format == "markdown":
        clean_format = "md"
    if clean_format not in SUPPORTED_EXPORT_FORMATS:
        raise ValueError(f"Export format must be one of: {', '.join(sorted(SUPPORTED_EXPORT_FORMATS))}")
    return clean_format


def write_history_csv(entries: list[HistoryEntry], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["created_at", "data", "output_path"])
        writer.writeheader()
        for entry in entries:
            writer.writerow(
                {
                    "created_at": entry.created_at,
                    "data": entry.data,
                    "output_path": entry.output_path,
                }
            )


def write_history_json(entries: list[HistoryEntry], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [
        {
            "created_at": entry.created_at,
            "data": entry.data,
            "output_path": entry.output_path,
        }
        for entry in entries
    ]
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_history_markdown(entries: list[HistoryEntry], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# QR Generation History",
        "",
        "| Created At | Data | Output Path |",
        "| --- | --- | --- |",
    ]
    for entry in entries:
        lines.append(f"| {entry.created_at} | {escape_markdown(entry.data)} | `{entry.output_path}` |")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_history_html(entries: list[HistoryEntry], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for entry in entries:
        rows.append(
            "<tr>"
            f"<td>{html.escape(entry.created_at)}</td>"
            f"<td>{html.escape(entry.data)}</td>"
            f"<td>{html.escape(entry.output_path)}</td>"
            "</tr>"
        )

    document = "\n".join(
        [
            "<!doctype html>",
            "<html lang=\"en\">",
            "<head>",
            "  <meta charset=\"utf-8\">",
            "  <title>QR Generation History</title>",
            "  <style>body{font-family:Arial,sans-serif;margin:24px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:8px;text-align:left}</style>",
            "</head>",
            "<body>",
            "  <h1>QR Generation History</h1>",
            "  <table>",
            "    <thead><tr><th>Created At</th><th>Data</th><th>Output Path</th></tr></thead>",
            "    <tbody>",
            *[f"      {row}" for row in rows],
            "    </tbody>",
            "  </table>",
            "</body>",
            "</html>",
        ]
    )
    output_path.write_text(document, encoding="utf-8")


def escape_markdown(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")
