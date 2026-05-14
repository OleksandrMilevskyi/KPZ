from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .batch import summarize_batch_results
from .generator import build_qr_options
from .profiles import profile_names
from .service import QRApplicationService
from .settings import format_settings
from .statistics import format_history_stats
from .templates import parse_template_values
from .backup import format_backup_result
from .diagnostics import diagnostics_passed, format_diagnostics
from .history_filters import HistoryQuery, format_history_entries

COMMAND_NAMES = {
    "single",
    "batch",
    "export-history",
    "stats",
    "profiles",
    "template",
    "report",
    "output-summary",
    "settings",
    "search-history",
    "diagnostics",
    "backup",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qr-app",
        description="Generate a QR code PNG image from text or a link.",
    )
    subparsers = parser.add_subparsers(dest="command")

    single_parser = subparsers.add_parser("single", help="Generate one QR code.")
    single_parser.add_argument("data", help="Text or link to encode into the QR code.")
    add_generation_options(single_parser)

    batch_parser = subparsers.add_parser("batch", help="Generate many QR codes from a text or CSV file.")
    batch_parser.add_argument("batch_file", help="Path to .txt or .csv file with QR data.")
    batch_parser.add_argument("--output-dir", default="output/batch", help="Folder for generated PNG files.")
    add_style_options(batch_parser)

    export_parser = subparsers.add_parser("export-history", help="Export generation history.")
    export_parser.add_argument("output", help="Output file path, for example output/history.csv.")
    export_parser.add_argument("--format", choices=["csv", "json", "md", "html"], help="Export format.")

    subparsers.add_parser("stats", help="Show generation history statistics.")
    subparsers.add_parser("profiles", help="List available style profiles.")

    template_parser = subparsers.add_parser("template", help="Generate QR code from a built-in template.")
    template_parser.add_argument("template_name", choices=["wifi", "email", "sms", "phone", "geo", "vcard"])
    template_parser.add_argument("values", nargs="*", help="Template values in key=value format.")
    add_generation_options(template_parser)

    report_parser = subparsers.add_parser("report", help="Create an HTML project report.")
    report_parser.add_argument("--output", default="output/report.html", help="Report output path.")

    output_parser = subparsers.add_parser("output-summary", help="Show generated output folder summary.")
    output_parser.add_argument("--output-dir", default="output", help="Folder to inspect.")

    subparsers.add_parser("settings", help="Show application settings.")

    search_parser = subparsers.add_parser("search-history", help="Search saved QR generation history.")
    search_parser.add_argument("--text", default="", help="Search in QR data.")
    search_parser.add_argument("--output", default="", help="Search in output paths.")
    search_parser.add_argument("--limit", type=int, default=10, help="Maximum number of rows to print.")

    subparsers.add_parser("diagnostics", help="Check local environment and project files.")

    backup_parser = subparsers.add_parser("backup", help="Create a backup of app data files.")
    backup_parser.add_argument("--output", default="output/qr-data-backup.zip", help="Backup archive path.")
    return parser


def add_generation_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-o",
        "--output",
        default="output/qr-code.png",
        help="Path to the PNG file that will be created.",
    )
    parser.add_argument("--profile", help="Use a saved style profile.")
    parser.add_argument("--no-history", action="store_true", help="Do not write this generation to history.")
    parser.add_argument("--no-overwrite", action="store_true", help="Create a unique file instead of overwriting.")
    parser.add_argument("--validate-url", action="store_true", help="Validate URL-like input before generation.")
    add_style_options(parser)


def add_style_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--box-size", type=int, default=10, help="Pixel size of each QR box.")
    parser.add_argument("--border", type=int, default=4, help="QR quiet-zone border size.")
    parser.add_argument("--fill", default="black", help="QR foreground color.")
    parser.add_argument("--back", default="white", help="QR background color.")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(normalize_argv(argv))
    service = QRApplicationService()

    try:
        if args.command == "batch":
            options = build_qr_options(args.box_size, args.border, args.fill, args.back)
            results = service.generate_from_batch_file(Path(args.batch_file), Path(args.output_dir), options)
            print(summarize_batch_results(results))
            return 0 if all(result.success for result in results) else 1

        if args.command == "export-history":
            result = service.export_history_file(Path(args.output), args.format)
            print(f"Exported {result.item_count} history items to {result.output_path}")
            return 0

        if args.command == "stats":
            print(format_history_stats(service.history_stats()))
            return 0

        if args.command == "profiles":
            print("Available profiles:")
            for name in profile_names():
                print(f"- {name}")
            return 0

        if args.command == "template":
            values = parse_template_values(args.values)
            options = build_qr_options(args.box_size, args.border, args.fill, args.back)
            output_path = service.generate_from_template(args.template_name, values, Path(args.output), options)
            print(f"QR code saved to: {output_path}")
            return 0

        if args.command == "report":
            output_path = service.build_report(Path(args.output))
            print(f"Report saved to: {output_path}")
            return 0

        if args.command == "output-summary":
            print(service.output_summary(Path(args.output_dir)))
            return 0

        if args.command == "settings":
            print(format_settings(service.settings()))
            return 0

        if args.command == "search-history":
            query = HistoryQuery(text=args.text, output_contains=args.output, limit=args.limit)
            print(format_history_entries(service.search_history(query)))
            return 0

        if args.command == "diagnostics":
            checks = service.diagnostics()
            print(format_diagnostics(checks))
            return 0 if diagnostics_passed(checks) else 1

        if args.command == "backup":
            result = service.backup_data(Path(args.output))
            print(format_backup_result(result, "Backup created"))
            return 0

        data = args.data

        if args.profile:
            output_path = service.generate_with_profile(
                data=data,
                output_path=Path(args.output),
                profile_name=args.profile,
                overwrite=not args.no_overwrite,
            )
        else:
            options = build_qr_options(args.box_size, args.border, args.fill, args.back)
            output_path = service.generate_single(
                data=data,
                output_path=Path(args.output),
                options=options,
                save_history=not args.no_history,
                overwrite=not args.no_overwrite,
                validate_url=args.validate_url,
            )
    except ValueError as error:
        parser.error(str(error))
        return 2

    print(f"QR code saved to: {output_path}")
    return 0


def normalize_argv(argv: list[str] | None) -> list[str] | None:
    if argv is None:
        argv = sys.argv[1:]
    if not argv or argv[0].startswith("-") or argv[0] in COMMAND_NAMES:
        return argv
    return ["single", *argv]
