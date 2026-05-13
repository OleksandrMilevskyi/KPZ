from __future__ import annotations

import csv
from pathlib import Path

from .filenames import build_output_path, unique_output_path
from .generator import QRCodeOptions, generate_qr_code
from .history import add_history_entry
from .models import BatchItem, BatchResult
from .validators import normalize_qr_data, validate_output_name


def parse_batch_file(path: Path) -> list[BatchItem]:
    if not path.exists():
        raise ValueError(f"Batch file does not exist: {path}")
    if path.suffix.lower() == ".csv":
        return parse_batch_csv(path)
    return parse_batch_lines(path)


def parse_batch_lines(path: Path) -> list[BatchItem]:
    items: list[BatchItem] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        items.append(BatchItem(data=normalize_qr_data(stripped)))
    if not items:
        raise ValueError("Batch file does not contain any QR data.")
    return items


def parse_batch_csv(path: Path) -> list[BatchItem]:
    items: list[BatchItem] = []
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or "data" not in reader.fieldnames:
            raise ValueError("CSV batch file must contain a 'data' column.")

        for row in reader:
            data = normalize_qr_data(row.get("data", ""))
            output_name = normalize_output_name(row.get("output_name"))
            items.append(BatchItem(data=data, output_name=output_name))

    if not items:
        raise ValueError("CSV batch file does not contain any QR data.")
    return items


def normalize_output_name(value: str | None) -> str | None:
    if value is None or not value.strip():
        return None
    return validate_output_name(value)


def generate_batch(
    items: list[BatchItem],
    output_dir: Path,
    options: QRCodeOptions | None = None,
    save_history: bool = True,
) -> list[BatchResult]:
    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[BatchResult] = []

    for item in items:
        output_path = unique_output_path(build_output_path(output_dir, item.data, item.output_name))
        try:
            result_path = generate_qr_code(item.data, output_path, options)
            if save_history:
                add_history_entry(item.data, result_path)
            results.append(BatchResult(data=item.data, output_path=result_path, success=True))
        except (OSError, ValueError) as error:
            results.append(BatchResult(data=item.data, output_path=output_path, success=False, error=str(error)))

    return results


def summarize_batch_results(results: list[BatchResult]) -> str:
    success_count = sum(1 for result in results if result.success)
    failed_count = len(results) - success_count
    lines = [f"Batch generation finished: {success_count} succeeded, {failed_count} failed."]

    for result in results:
        status = "OK" if result.success else "ERROR"
        message = str(result.output_path) if result.success else result.error or "Unknown error"
        lines.append(f"[{status}] {result.data} -> {message}")

    return "\n".join(lines)
