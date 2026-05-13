from pathlib import Path

from qr_app.generator import QRCodeOptions
from qr_app.models import StyleProfile
from qr_app.profiles import find_profile, load_profiles, profile_names, save_profiles, upsert_profile


def test_load_profiles_returns_defaults_when_file_is_missing(tmp_path: Path) -> None:
    profiles = load_profiles(tmp_path / "missing.json")

    assert "classic" in [profile.name for profile in profiles]


def test_save_and_find_profile_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "profiles.json"
    profile = StyleProfile(
        name="dark",
        description="Dark profile",
        options=QRCodeOptions(box_size=8, border=3, fill_color="white", back_color="black"),
    )

    save_profiles([profile], path)

    assert find_profile("dark", path) == profile


def test_upsert_profile_replaces_existing_profile(tmp_path: Path) -> None:
    path = tmp_path / "profiles.json"
    old_profile = StyleProfile(name="custom", options=QRCodeOptions(box_size=8))
    new_profile = StyleProfile(name="custom", options=QRCodeOptions(box_size=12))

    save_profiles([old_profile], path)
    profiles = upsert_profile(new_profile, path)

    assert profiles == [new_profile]


def test_profile_names_returns_names(tmp_path: Path) -> None:
    path = tmp_path / "profiles.json"
    save_profiles([StyleProfile(name="one", options=QRCodeOptions())], path)

    assert profile_names(path) == ["one"]
