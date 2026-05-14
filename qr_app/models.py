from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .generator import QRCodeOptions


@dataclass(frozen=True)
class BatchItem:
    data: str
    output_name: str | None = None


@dataclass(frozen=True)
class BatchResult:
    data: str
    output_path: Path
    success: bool
    error: str | None = None


@dataclass(frozen=True)
class StyleProfile:
    name: str
    options: QRCodeOptions
    description: str = ""


@dataclass(frozen=True)
class HistoryStats:
    total_items: int
    unique_outputs: int
    first_created_at: str | None
    last_created_at: str | None
    longest_data: str | None


@dataclass(frozen=True)
class ExportResult:
    output_path: Path
    item_count: int
    format_name: str
