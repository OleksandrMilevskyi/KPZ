from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import qrcode
from qrcode.constants import ERROR_CORRECT_M

from .validators import normalize_color, normalize_qr_data, validate_border, validate_box_size


@dataclass(frozen=True)
class QRCodeOptions:
    box_size: int = 10
    border: int = 4
    fill_color: str = "black"
    back_color: str = "white"


def build_qr_options(
    box_size: int,
    border: int,
    fill_color: str = "black",
    back_color: str = "white",
) -> QRCodeOptions:
    return QRCodeOptions(
        box_size=validate_box_size(box_size),
        border=validate_border(border),
        fill_color=normalize_color(fill_color, "black"),
        back_color=normalize_color(back_color, "white"),
    )


def generate_qr_code(data: str, output_path: Path, options: QRCodeOptions | None = None) -> Path:
    image = create_qr_image(data, options)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    return output_path.resolve()


def create_qr_image(data: str, options: QRCodeOptions | None = None) -> Any:
    clean_data = normalize_qr_data(data)

    options = options or QRCodeOptions()
    options = build_qr_options(
        box_size=options.box_size,
        border=options.border,
        fill_color=options.fill_color,
        back_color=options.back_color,
    )

    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=options.box_size,
        border=options.border,
    )
    qr.add_data(clean_data)
    qr.make(fit=True)

    return qr.make_image(fill_color=options.fill_color, back_color=options.back_color)
