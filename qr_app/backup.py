from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


BACKUP_FILE_NAMES = [
    "history.json",
    "profiles.json",
    "settings.json",
    "audit-log.jsonl",
]


@dataclass(frozen=True)
class BackupResult:
    archive_path: Path
    file_count: int


def create_backup(output_dir: Path = Path("output"), archive_path: Path = Path("output/qr-data-backup.zip")) -> BackupResult:
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    file_count = 0

    with ZipFile(archive_path, "w", ZIP_DEFLATED) as archive:
        for file_name in BACKUP_FILE_NAMES:
            source = output_dir / file_name
            if source.exists() and source.is_file():
                archive.write(source, arcname=file_name)
                file_count += 1

    return BackupResult(archive_path=archive_path.resolve(), file_count=file_count)


def restore_backup(archive_path: Path, output_dir: Path = Path("output")) -> BackupResult:
    if not archive_path.exists():
        raise ValueError(f"Backup archive does not exist: {archive_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    restored_count = 0
    with ZipFile(archive_path, "r") as archive:
        for name in archive.namelist():
            if name not in BACKUP_FILE_NAMES:
                continue
            archive.extract(name, output_dir)
            restored_count += 1

    return BackupResult(archive_path=archive_path.resolve(), file_count=restored_count)


def list_backup_contents(archive_path: Path) -> list[str]:
    if not archive_path.exists():
        raise ValueError(f"Backup archive does not exist: {archive_path}")
    with ZipFile(archive_path, "r") as archive:
        return [name for name in archive.namelist() if name in BACKUP_FILE_NAMES]


def format_backup_result(result: BackupResult, action: str) -> str:
    return f"{action}: {result.file_count} files, archive: {result.archive_path}"
