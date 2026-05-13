from __future__ import annotations

import argparse
from pathlib import Path

from .generator import QRCodeOptions, generate_qr_code


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qr-app",
        description="Generate a QR code PNG image from text or a link.",
    )
    parser.add_argument("data", help="Text or link to encode into the QR code.")
    parser.add_argument(
        "-o",
        "--output",
        default="output/qr-code.png",
        help="Path to the PNG file that will be created.",
    )
    parser.add_argument("--box-size", type=int, default=10, help="Pixel size of each QR box.")
    parser.add_argument("--border", type=int, default=4, help="QR quiet-zone border size.")
    parser.add_argument("--fill", default="black", help="QR foreground color.")
    parser.add_argument("--back", default="white", help="QR background color.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    options = QRCodeOptions(
        box_size=args.box_size,
        border=args.border,
        fill_color=args.fill,
        back_color=args.back,
    )

    try:
        output_path = generate_qr_code(args.data, Path(args.output), options)
    except ValueError as error:
        parser.error(str(error))
        return 2

    print(f"QR code saved to: {output_path}")
    return 0
