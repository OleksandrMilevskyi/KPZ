from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .generator import QRCodeOptions, build_qr_options
from .models import StyleProfile


DEFAULT_PROFILES_PATH = Path("output/profiles.json")


DEFAULT_PROFILES = [
    StyleProfile(
        name="classic",
        description="High-contrast black QR code on white background.",
        options=QRCodeOptions(box_size=10, border=4, fill_color="black", back_color="white"),
    ),
    StyleProfile(
        name="compact",
        description="Smaller QR code for quick exports.",
        options=QRCodeOptions(box_size=7, border=2, fill_color="black", back_color="white"),
    ),
    StyleProfile(
        name="presentation",
        description="Larger QR code for reports and slides.",
        options=QRCodeOptions(box_size=14, border=5, fill_color="#111111", back_color="#ffffff"),
    ),
]


def load_profiles(path: Path = DEFAULT_PROFILES_PATH) -> list[StyleProfile]:
    if not path.exists():
        return list(DEFAULT_PROFILES)

    try:
        raw_profiles = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return list(DEFAULT_PROFILES)

    if not isinstance(raw_profiles, list):
        return list(DEFAULT_PROFILES)

    profiles: list[StyleProfile] = []
    for item in raw_profiles:
        profile = parse_profile(item)
        if profile is not None:
            profiles.append(profile)

    return profiles or list(DEFAULT_PROFILES)


def save_profiles(profiles: list[StyleProfile], path: Path = DEFAULT_PROFILES_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [
        {
            "name": profile.name,
            "description": profile.description,
            "options": asdict(profile.options),
        }
        for profile in profiles
    ]
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def find_profile(name: str, path: Path = DEFAULT_PROFILES_PATH) -> StyleProfile:
    clean_name = name.strip().lower()
    for profile in load_profiles(path):
        if profile.name.lower() == clean_name:
            return profile
    raise ValueError(f"Unknown style profile: {name}")


def upsert_profile(profile: StyleProfile, path: Path = DEFAULT_PROFILES_PATH) -> list[StyleProfile]:
    profiles = load_profiles(path)
    updated: list[StyleProfile] = []
    was_updated = False

    for existing in profiles:
        if existing.name.lower() == profile.name.lower():
            updated.append(profile)
            was_updated = True
        else:
            updated.append(existing)

    if not was_updated:
        updated.append(profile)

    save_profiles(updated, path)
    return updated


def parse_profile(item: Any) -> StyleProfile | None:
    if not isinstance(item, dict):
        return None

    name = item.get("name")
    description = item.get("description", "")
    options = item.get("options")
    if not isinstance(name, str) or not isinstance(description, str) or not isinstance(options, dict):
        return None

    try:
        qr_options = build_qr_options(
            box_size=int(options.get("box_size", 10)),
            border=int(options.get("border", 4)),
            fill_color=str(options.get("fill_color", "black")),
            back_color=str(options.get("back_color", "white")),
        )
    except (TypeError, ValueError):
        return None

    return StyleProfile(name=name.strip(), description=description.strip(), options=qr_options)


def profile_names(path: Path = DEFAULT_PROFILES_PATH) -> list[str]:
    return [profile.name for profile in load_profiles(path)]
