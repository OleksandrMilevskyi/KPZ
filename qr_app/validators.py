from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse


HEX_COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")
NAMED_COLOR_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9 _-]{0,31}$")
SAFE_FILENAME_PATTERN = re.compile(r"^[a-zA-Z0-9._ -]+$")


def normalize_qr_data(data: str) -> str:
    normalized = data.strip()
    if not normalized:
        raise ValueError("QR data cannot be empty.")
    return normalized


def validate_url_if_present(data: str) -> str:
    normalized = normalize_qr_data(data)
    if "://" not in normalized:
        return normalized

    parsed = urlparse(normalized)
    if parsed.scheme not in {"http", "https", "mailto", "tel"}:
        raise ValueError("Only http, https, mailto, and tel URLs are supported.")
    if parsed.scheme in {"http", "https"} and not parsed.netloc:
        raise ValueError("URL must contain a host name.")
    return normalized


def normalize_color(value: str, fallback: str) -> str:
    color = value.strip()
    if not color:
        return fallback
    if HEX_COLOR_PATTERN.match(color):
        return color
    if NAMED_COLOR_PATTERN.match(color):
        return color
    raise ValueError(f"Invalid color value: {value}")


def validate_box_size(box_size: int) -> int:
    if box_size <= 0:
        raise ValueError("Box size must be greater than zero.")
    if box_size > 60:
        raise ValueError("Box size is too large.")
    return box_size


def validate_border(border: int) -> int:
    if border < 0:
        raise ValueError("Border cannot be negative.")
    if border > 40:
        raise ValueError("Border is too large.")
    return border


def ensure_png_path(path: Path) -> Path:
    if path.suffix.lower() != ".png":
        return path.with_suffix(".png")
    return path


def validate_output_name(name: str) -> str:
    clean_name = name.strip()
    if not clean_name:
        raise ValueError("Output name cannot be empty.")
    if "/" in clean_name or "\\" in clean_name:
        raise ValueError("Output name cannot contain path separators.")
    if not SAFE_FILENAME_PATTERN.match(clean_name):
        raise ValueError("Output name contains unsupported characters.")
    return clean_name
