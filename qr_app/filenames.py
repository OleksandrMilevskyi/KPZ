from __future__ import annotations

import re
from pathlib import Path

from .validators import ensure_png_path


SLUG_PATTERN = re.compile(r"[^a-zA-Z0-9]+")


def slugify(value: str, fallback: str = "qr-code") -> str:
    slug = SLUG_PATTERN.sub("-", value.strip().lower()).strip("-")
    return slug[:60] or fallback


def build_output_path(output_dir: Path, data: str, output_name: str | None = None) -> Path:
    if output_name:
        return ensure_png_path(output_dir / output_name)
    return ensure_png_path(output_dir / slugify(data))


def unique_output_path(path: Path) -> Path:
    path = ensure_png_path(path)
    if not path.exists():
        return path

    counter = 2
    while True:
        candidate = path.with_name(f"{path.stem}-{counter}{path.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def display_path(path: Path, max_length: int = 80) -> str:
    text = str(path)
    if len(text) <= max_length:
        return text
    return f"...{text[-(max_length - 3):]}"
