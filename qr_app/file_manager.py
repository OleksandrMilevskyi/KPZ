from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class OutputFileInfo:
    path: Path
    size_bytes: int
    modified_at: float


def list_output_files(output_dir: Path, suffix: str = ".png") -> list[OutputFileInfo]:
    if not output_dir.exists():
        return []

    files: list[OutputFileInfo] = []
    for path in output_dir.rglob(f"*{suffix}"):
        if not path.is_file():
            continue
        stat = path.stat()
        files.append(OutputFileInfo(path=path, size_bytes=stat.st_size, modified_at=stat.st_mtime))
    return sorted(files, key=lambda item: item.modified_at, reverse=True)


def calculate_output_size(output_dir: Path) -> int:
    return sum(file_info.size_bytes for file_info in list_output_files(output_dir))


def find_old_output_files(output_dir: Path, keep_latest: int) -> list[OutputFileInfo]:
    if keep_latest < 0:
        raise ValueError("keep_latest cannot be negative.")
    files = list_output_files(output_dir)
    return files[keep_latest:]


def delete_output_files(files: list[OutputFileInfo]) -> int:
    deleted_count = 0
    for file_info in files:
        try:
            file_info.path.unlink()
            deleted_count += 1
        except FileNotFoundError:
            continue
    return deleted_count


def format_file_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024 * 1024):.1f} MB"


def summarize_output_folder(output_dir: Path) -> str:
    files = list_output_files(output_dir)
    total_size = calculate_output_size(output_dir)
    lines = [
        f"Output folder: {output_dir}",
        f"PNG files: {len(files)}",
        f"Total size: {format_file_size(total_size)}",
    ]
    for file_info in files[:10]:
        lines.append(f"- {file_info.path.name}: {format_file_size(file_info.size_bytes)}")
    return "\n".join(lines)
