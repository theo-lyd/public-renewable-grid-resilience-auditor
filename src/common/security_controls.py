from __future__ import annotations

import json
import re
from typing import Any

SENSITIVE_KEY_HINTS = ("password", "secret", "token", "api_key", "apikey", "credential")
DATA_CLASSIFICATIONS = {"public", "internal", "restricted"}
PLAINTEXT_SECRET_REGEX = re.compile(
    r"['\"]?(api[_-]?key|token|password|secret)['\"]?\s*[:=]\s*['\"]?[^'\"\s,}]+",
    flags=re.IGNORECASE,
)


def is_sensitive_key(key: str) -> bool:
    normalized = key.lower()
    return any(hint in normalized for hint in SENSITIVE_KEY_HINTS)


def redact_sensitive_values(payload: dict[str, Any]) -> dict[str, Any]:
    redacted: dict[str, Any] = {}
    for key, value in payload.items():
        if is_sensitive_key(key):
            redacted[key] = "***REDACTED***"
        else:
            redacted[key] = value

    return redacted


def validate_data_classification(classification: str, public_only: bool = True) -> bool:
    if classification not in DATA_CLASSIFICATIONS:
        raise ValueError(f"Unsupported classification: {classification}")

    if public_only and classification != "public":
        raise PermissionError("This project is configured for public-sector public datasets only.")

    return True


def detect_plaintext_secrets_in_text(content: str) -> list[str]:
    matches = {token.lower().replace("-", "_") for token in PLAINTEXT_SECRET_REGEX.findall(content)}
    return sorted(matches)


def main() -> None:
    sample = {
        "entsoe_api_key": "abc123",
        "dataset": "public_renewable_mix",
        "owner": "grid-analytics",
    }

    result = {
        "redacted_preview": redact_sensitive_values(sample),
        "classification_check": validate_data_classification("public", public_only=True),
        "plaintext_findings": detect_plaintext_secrets_in_text("dataset=public"),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
