from pathlib import Path

from qr_app.audit import append_audit_event, create_audit_event, load_audit_events, parse_audit_event, record_generation_audit


def test_create_audit_event_sets_metadata() -> None:
    event = create_audit_event("test", "message", {"key": "value"})

    assert event.event_type == "test"
    assert event.metadata == {"key": "value"}


def test_append_and_load_audit_event_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "audit.jsonl"
    event = create_audit_event("test", "message")

    append_audit_event(event, path)

    assert load_audit_events(path) == [event]


def test_parse_audit_event_ignores_broken_json() -> None:
    assert parse_audit_event("{broken") is None


def test_record_generation_audit_writes_event(tmp_path: Path) -> None:
    path = tmp_path / "audit.jsonl"

    record_generation_audit("hello", tmp_path / "hello.png", path)

    events = load_audit_events(path)
    assert events[0].event_type == "generate"
