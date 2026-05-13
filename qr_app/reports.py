from __future__ import annotations

import html
from pathlib import Path

from .file_manager import list_output_files
from .history import load_history
from .statistics import calculate_history_stats


def build_project_report(output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    history = load_history()
    stats = calculate_history_stats(history)
    files = list_output_files(Path("output"))

    document = "\n".join(
        [
            "<!doctype html>",
            "<html lang=\"en\">",
            "<head>",
            "  <meta charset=\"utf-8\">",
            "  <title>QR Code Generator Report</title>",
            "  <style>",
            "    body { font-family: Arial, sans-serif; margin: 32px; color: #1f2937; }",
            "    table { border-collapse: collapse; width: 100%; margin-top: 12px; }",
            "    th, td { border: 1px solid #d1d5db; padding: 8px; text-align: left; }",
            "    th { background: #f3f4f6; }",
            "    .metric { display: inline-block; margin-right: 16px; padding: 12px; border: 1px solid #d1d5db; }",
            "  </style>",
            "</head>",
            "<body>",
            "  <h1>QR Code Generator Report</h1>",
            "  <section>",
            "    <h2>Summary</h2>",
            f"    <div class=\"metric\"><strong>Total history items:</strong> {stats.total_items}</div>",
            f"    <div class=\"metric\"><strong>Unique output files:</strong> {stats.unique_outputs}</div>",
            f"    <div class=\"metric\"><strong>Generated PNG files:</strong> {len(files)}</div>",
            "  </section>",
            "  <section>",
            "    <h2>History</h2>",
            build_history_table(history),
            "  </section>",
            "  <section>",
            "    <h2>Output Files</h2>",
            build_files_table(files),
            "  </section>",
            "</body>",
            "</html>",
        ]
    )
    output_path.write_text(document, encoding="utf-8")
    return output_path.resolve()


def build_history_table(history: list) -> str:
    if not history:
        return "<p>No history records yet.</p>"

    rows = []
    for entry in history:
        rows.append(
            "<tr>"
            f"<td>{html.escape(entry.created_at)}</td>"
            f"<td>{html.escape(entry.data)}</td>"
            f"<td>{html.escape(entry.output_path)}</td>"
            "</tr>"
        )
    return (
        "<table><thead><tr><th>Created At</th><th>Data</th><th>Output Path</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )


def build_files_table(files: list) -> str:
    if not files:
        return "<p>No generated PNG files found.</p>"

    rows = []
    for file_info in files:
        rows.append(
            "<tr>"
            f"<td>{html.escape(file_info.path.name)}</td>"
            f"<td>{file_info.size_bytes}</td>"
            f"<td>{file_info.modified_at}</td>"
            "</tr>"
        )
    return "<table><thead><tr><th>Name</th><th>Size</th><th>Modified</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
