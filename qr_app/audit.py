from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_AUDIT_PATH = Path("output/audit-log.jsonl")


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    message: str
    created_at: str
    metadata: dict[str, str]


def create_audit_event(event_type: str, message: str, metadata: dict[str, str] | None = None) -> AuditEvent:
    return AuditEvent(
        event_type=event_type.strip() or "event",
        message=message.strip(),
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        metadata=metadata or {},
    )


def append_audit_event(event: AuditEvent, path: Path = DEFAULT_AUDIT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(asdict(event), ensure_ascii=False) + "\n")


def load_audit_events(path: Path = DEFAULT_AUDIT_PATH) -> list[AuditEvent]:
    if not path.exists():
        return []

    events: list[AuditEvent] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        event = parse_audit_event(line)
        if event is not None:
            events.append(event)
    return events


def parse_audit_event(line: str) -> AuditEvent | None:
    try:
        raw_event: Any = json.loads(line)
    except json.JSONDecodeError:
        return None

    if not isinstance(raw_event, dict):
        return None
    event_type = raw_event.get("event_type")
    message = raw_event.get("message")
    created_at = raw_event.get("created_at")
    metadata = raw_event.get("metadata", {})
    if not isinstance(event_type, str) or not isinstance(message, str) or not isinstance(created_at, str):
        return None
    if not isinstance(metadata, dict):
        metadata = {}

    return AuditEvent(
        event_type=event_type,
        message=message,
        created_at=created_at,
        metadata={str(key): str(value) for key, value in metadata.items()},
    )


def record_generation_audit(data: str, output_path: Path, path: Path = DEFAULT_AUDIT_PATH) -> None:
    event = create_audit_event(
        "generate",
        "Generated QR code",
        {
            "data": data[:120],
            "output_path": str(output_path),
        },
    )
    append_audit_event(event, path)
