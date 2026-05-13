from __future__ import annotations

from pathlib import Path

from .audit import record_generation_audit
from .backup import BackupResult, create_backup
from .batch import generate_batch, parse_batch_file
from .diagnostics import DiagnosticCheck, run_diagnostics
from .exporters import export_history
from .file_manager import summarize_output_folder
from .filenames import unique_output_path
from .generator import QRCodeOptions, generate_qr_code
from .history import add_history_entry, load_history
from .history_filters import HistoryQuery, search_history
from .models import BatchResult, ExportResult, HistoryStats
from .profiles import find_profile
from .reports import build_project_report
from .settings import AppSettings, load_settings
from .statistics import calculate_history_stats
from .templates import render_template
from .validators import ensure_png_path, validate_url_if_present


class QRApplicationService:
    def generate_single(
        self,
        data: str,
        output_path: Path,
        options: QRCodeOptions | None = None,
        save_history: bool = True,
        overwrite: bool = True,
        validate_url: bool = False,
    ) -> Path:
        clean_data = validate_url_if_present(data) if validate_url else data
        clean_path = ensure_png_path(output_path)
        if not overwrite:
            clean_path = unique_output_path(clean_path)

        result = generate_qr_code(clean_data, clean_path, options)
        if save_history:
            add_history_entry(clean_data, result)
        record_generation_audit(clean_data, result)
        return result

    def generate_with_profile(
        self,
        data: str,
        output_path: Path,
        profile_name: str,
        overwrite: bool = True,
    ) -> Path:
        profile = find_profile(profile_name)
        return self.generate_single(data, output_path, profile.options, overwrite=overwrite)

    def generate_from_batch_file(
        self,
        batch_file: Path,
        output_dir: Path,
        options: QRCodeOptions | None = None,
    ) -> list[BatchResult]:
        items = parse_batch_file(batch_file)
        return generate_batch(items, output_dir, options)

    def export_history_file(self, output_path: Path, format_name: str | None = None) -> ExportResult:
        return export_history(output_path, format_name)

    def history_stats(self) -> HistoryStats:
        return calculate_history_stats(load_history())

    def generate_from_template(
        self,
        template_name: str,
        values: dict[str, str],
        output_path: Path,
        options: QRCodeOptions | None = None,
    ) -> Path:
        data = render_template(template_name, values)
        return self.generate_single(data, output_path, options)

    def build_report(self, output_path: Path) -> Path:
        return build_project_report(output_path)

    def output_summary(self, output_dir: Path = Path("output")) -> str:
        return summarize_output_folder(output_dir)

    def settings(self) -> AppSettings:
        return load_settings()

    def search_history(self, query: HistoryQuery):
        return search_history(query)

    def diagnostics(self) -> list[DiagnosticCheck]:
        return run_diagnostics()

    def backup_data(self, archive_path: Path = Path("output/qr-data-backup.zip")) -> BackupResult:
        return create_backup(archive_path=archive_path)
