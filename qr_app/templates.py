from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote

from .validators import normalize_qr_data


@dataclass(frozen=True)
class WifiTemplate:
    ssid: str
    password: str = ""
    security: str = "WPA"
    hidden: bool = False

    def render(self) -> str:
        clean_ssid = escape_wifi_value(normalize_qr_data(self.ssid))
        clean_password = escape_wifi_value(self.password.strip())
        clean_security = self.security.strip().upper() or "nopass"
        hidden_value = "true" if self.hidden else "false"
        return f"WIFI:T:{clean_security};S:{clean_ssid};P:{clean_password};H:{hidden_value};;"


@dataclass(frozen=True)
class EmailTemplate:
    email: str
    subject: str = ""
    body: str = ""

    def render(self) -> str:
        clean_email = normalize_qr_data(self.email)
        params = []
        if self.subject:
            params.append(f"subject={quote(self.subject)}")
        if self.body:
            params.append(f"body={quote(self.body)}")
        query = f"?{'&'.join(params)}" if params else ""
        return f"mailto:{clean_email}{query}"


@dataclass(frozen=True)
class SmsTemplate:
    phone: str
    message: str = ""

    def render(self) -> str:
        clean_phone = normalize_qr_data(self.phone)
        if not self.message:
            return f"sms:{clean_phone}"
        return f"sms:{clean_phone}?body={quote(self.message)}"


@dataclass(frozen=True)
class PhoneTemplate:
    phone: str

    def render(self) -> str:
        return f"tel:{normalize_qr_data(self.phone)}"


@dataclass(frozen=True)
class GeoTemplate:
    latitude: float
    longitude: float
    label: str = ""

    def render(self) -> str:
        if not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90.")
        if not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180.")
        base = f"geo:{self.latitude},{self.longitude}"
        if not self.label:
            return base
        return f"{base}?q={self.latitude},{self.longitude}({quote(self.label)})"


@dataclass(frozen=True)
class VCardTemplate:
    full_name: str
    phone: str = ""
    email: str = ""
    organization: str = ""
    title: str = ""
    website: str = ""

    def render(self) -> str:
        lines = [
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"FN:{normalize_qr_data(self.full_name)}",
        ]
        if self.organization:
            lines.append(f"ORG:{self.organization.strip()}")
        if self.title:
            lines.append(f"TITLE:{self.title.strip()}")
        if self.phone:
            lines.append(f"TEL:{self.phone.strip()}")
        if self.email:
            lines.append(f"EMAIL:{self.email.strip()}")
        if self.website:
            lines.append(f"URL:{self.website.strip()}")
        lines.append("END:VCARD")
        return "\n".join(lines)


def escape_wifi_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace(":", "\\:")


def render_template(template_name: str, values: dict[str, str]) -> str:
    name = template_name.strip().lower()
    if name == "wifi":
        return WifiTemplate(
            ssid=values.get("ssid", ""),
            password=values.get("password", ""),
            security=values.get("security", "WPA"),
            hidden=parse_bool(values.get("hidden", "false")),
        ).render()
    if name == "email":
        return EmailTemplate(
            email=values.get("email", ""),
            subject=values.get("subject", ""),
            body=values.get("body", ""),
        ).render()
    if name == "sms":
        return SmsTemplate(phone=values.get("phone", ""), message=values.get("message", "")).render()
    if name == "phone":
        return PhoneTemplate(phone=values.get("phone", "")).render()
    if name == "geo":
        return GeoTemplate(
            latitude=float(values.get("latitude", "0")),
            longitude=float(values.get("longitude", "0")),
            label=values.get("label", ""),
        ).render()
    if name == "vcard":
        return VCardTemplate(
            full_name=values.get("full_name", ""),
            phone=values.get("phone", ""),
            email=values.get("email", ""),
            organization=values.get("organization", ""),
            title=values.get("title", ""),
            website=values.get("website", ""),
        ).render()
    raise ValueError(f"Unknown QR template: {template_name}")


def parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def parse_template_values(raw_values: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_value in raw_values:
        if "=" not in raw_value:
            raise ValueError("Template values must use key=value format.")
        key, value = raw_value.split("=", 1)
        clean_key = key.strip()
        if not clean_key:
            raise ValueError("Template value key cannot be empty.")
        values[clean_key] = value.strip()
    return values
