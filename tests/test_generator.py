from pathlib import Path

import pytest

from qr_app.generator import QRCodeOptions, build_qr_options, create_qr_image, generate_qr_code


def test_generate_qr_code_creates_png(tmp_path: Path) -> None:
    output_path = tmp_path / "qr.png"

    result = generate_qr_code("https://example.com", output_path)

    assert result == output_path.resolve()
    assert output_path.exists()
    assert output_path.read_bytes().startswith(b"\x89PNG")


def test_create_qr_image_returns_image_object() -> None:
    image = create_qr_image("preview")

    assert image.size[0] > 0
    assert image.size[1] > 0


def test_generate_qr_code_rejects_empty_data(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        generate_qr_code("   ", tmp_path / "qr.png")


def test_generate_qr_code_rejects_invalid_options(tmp_path: Path) -> None:
    options = QRCodeOptions(box_size=0)

    with pytest.raises(ValueError, match="greater than zero"):
        generate_qr_code("hello", tmp_path / "qr.png", options)


def test_build_qr_options_normalizes_blank_colors() -> None:
    options = build_qr_options(box_size=8, border=2, fill_color="  ", back_color="")

    assert options == QRCodeOptions(box_size=8, border=2, fill_color="black", back_color="white")


def test_build_qr_options_rejects_negative_border() -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        build_qr_options(box_size=8, border=-1)
