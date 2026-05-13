from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_M


@dataclass(frozen=True)
class QRCodeOptions:
    box_size: int = 10
    border: int = 4
    fill_color: str = "black"
    back_color: str = "white"


def generate_qr_code(data: str, output_path: Path, options: QRCodeOptions | None = None) -> Path:
    clean_data = data.strip()
    if not clean_data:
        raise ValueError("QR data cannot be empty.")

    options = options or QRCodeOptions()
    if options.box_size <= 0:
        raise ValueError("Box size must be greater than zero.")
    if options.border < 0:
        raise ValueError("Border cannot be negative.")

    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=options.box_size,
        border=options.border,
    )
    qr.add_data(clean_data)
    qr.make(fit=True)

    image = qr.make_image(fill_color=options.fill_color, back_color=options.back_color)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    return output_path.resolve()
