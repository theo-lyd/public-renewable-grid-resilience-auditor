import pytest

from src.common.security_controls import (
    detect_plaintext_secrets_in_text,
    is_sensitive_key,
    redact_sensitive_values,
    validate_data_classification,
)


def test_is_sensitive_key() -> None:
    assert is_sensitive_key("ENTSOE_API_KEY")
    assert not is_sensitive_key("zone_code")


def test_redact_sensitive_values() -> None:
    payload = {"api_key": "abc", "dataset": "public"}
    redacted = redact_sensitive_values(payload)
    assert redacted["api_key"] == "***REDACTED***"
    assert redacted["dataset"] == "public"


def test_validate_data_classification() -> None:
    assert validate_data_classification("public", public_only=True)

    with pytest.raises(PermissionError):
        validate_data_classification("restricted", public_only=True)

    with pytest.raises(ValueError):
        validate_data_classification("unknown", public_only=True)


def test_detect_plaintext_secrets_in_text() -> None:
    findings = detect_plaintext_secrets_in_text("api_key=abc and password=123")
    assert "api_key=" in findings
    assert "password=" in findings
