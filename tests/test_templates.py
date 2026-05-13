import pytest

from qr_app.templates import (
    EmailTemplate,
    GeoTemplate,
    PhoneTemplate,
    SmsTemplate,
    VCardTemplate,
    WifiTemplate,
    parse_bool,
    parse_template_values,
    render_template,
)


def test_wifi_template_escapes_special_characters() -> None:
    template = WifiTemplate(ssid="Cafe;WiFi", password="a:b,c")

    assert template.render() == "WIFI:T:WPA;S:Cafe\\;WiFi;P:a\\:b\\,c;H:false;;"


def test_email_template_adds_query_parameters() -> None:
    template = EmailTemplate(email="user@example.com", subject="Hello world", body="Line one")

    assert template.render() == "mailto:user@example.com?subject=Hello%20world&body=Line%20one"


def test_sms_and_phone_templates() -> None:
    assert SmsTemplate(phone="+380000000000", message="Hi").render() == "sms:+380000000000?body=Hi"
    assert PhoneTemplate(phone="+380000000000").render() == "tel:+380000000000"


def test_geo_template_validates_coordinates() -> None:
    assert GeoTemplate(latitude=50.45, longitude=30.52, label="Kyiv").render().startswith("geo:50.45,30.52")
    with pytest.raises(ValueError, match="Latitude"):
        GeoTemplate(latitude=100, longitude=30.52).render()


def test_vcard_template_renders_optional_fields() -> None:
    template = VCardTemplate(full_name="Alex", phone="+1", email="a@example.com", organization="KPZ")

    rendered = template.render()

    assert "BEGIN:VCARD" in rendered
    assert "ORG:KPZ" in rendered


def test_render_template_dispatches_by_name() -> None:
    assert render_template("phone", {"phone": "+1"}) == "tel:+1"


def test_render_template_rejects_unknown_template() -> None:
    with pytest.raises(ValueError, match="Unknown"):
        render_template("unknown", {})


def test_parse_bool_understands_common_values() -> None:
    assert parse_bool("yes") is True
    assert parse_bool("off") is False


def test_parse_template_values_reads_key_value_pairs() -> None:
    assert parse_template_values(["ssid=Home", "password=secret"]) == {"ssid": "Home", "password": "secret"}


def test_parse_template_values_rejects_invalid_pairs() -> None:
    with pytest.raises(ValueError, match="key=value"):
        parse_template_values(["broken"])
