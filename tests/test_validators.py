from pathlib import Path

import pytest

from qr_app.validators import (
    ensure_png_path,
    normalize_color,
    normalize_qr_data,
    validate_output_name,
    validate_url_if_present,
)


def test_normalize_qr_data_strips_text() -> None:
    assert normalize_qr_data("  hello  ") == "hello"


def test_normalize_qr_data_rejects_blank_text() -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        normalize_qr_data("   ")


def test_validate_url_if_present_accepts_plain_text() -> None:
    assert validate_url_if_present("plain text") == "plain text"


def test_validate_url_if_present_rejects_url_without_host() -> None:
    with pytest.raises(ValueError, match="host"):
        validate_url_if_present("https://")


def test_normalize_color_accepts_hex_and_named_colors() -> None:
    assert normalize_color("#abcdef", "black") == "#abcdef"
    assert normalize_color("navy", "black") == "navy"


def test_normalize_color_uses_fallback_for_blank_value() -> None:
    assert normalize_color("  ", "white") == "white"


def test_normalize_color_rejects_invalid_value() -> None:
    with pytest.raises(ValueError, match="Invalid color"):
        normalize_color("not/a/color", "black")


def test_ensure_png_path_adds_png_suffix() -> None:
    assert ensure_png_path(Path("sample")).name == "sample.png"


def test_validate_output_name_rejects_paths() -> None:
    with pytest.raises(ValueError, match="path separators"):
        validate_output_name("../bad.png")
