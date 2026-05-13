from pathlib import Path

from qr_app.service import QRApplicationService


def test_service_generate_single_creates_png(tmp_path: Path) -> None:
    service = QRApplicationService()
    output_path = tmp_path / "single.png"

    result = service.generate_single("hello", output_path, save_history=False)

    assert result == output_path.resolve()
    assert output_path.exists()


def test_service_generate_single_can_avoid_overwrite(tmp_path: Path) -> None:
    service = QRApplicationService()
    output_path = tmp_path / "single.png"
    output_path.write_text("existing", encoding="utf-8")

    result = service.generate_single("hello", output_path, save_history=False, overwrite=False)

    assert result.name == "single-2.png"


def test_service_generate_from_batch_file(tmp_path: Path) -> None:
    service = QRApplicationService()
    batch_file = tmp_path / "items.txt"
    batch_file.write_text("one\ntwo\n", encoding="utf-8")

    results = service.generate_from_batch_file(batch_file, tmp_path / "out")

    assert len(results) == 2
    assert all(result.success for result in results)
