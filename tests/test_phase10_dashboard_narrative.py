from src.monitoring.dashboard_narrative import METRIC_CATALOG, validate_metric_catalog


def test_metric_catalog_has_required_fields() -> None:
    for card in METRIC_CATALOG.values():
        assert card.metric_id
        assert card.title
        assert card.plain_language_explanation
        assert card.technical_definition
        assert card.caveat


def test_validate_metric_catalog_success() -> None:
    required = set(METRIC_CATALOG.keys())
    result = validate_metric_catalog(required)
    assert result["is_valid"] is True
    assert result["missing_metric_ids"] == []


def test_validate_metric_catalog_missing_metric() -> None:
    result = validate_metric_catalog({"renewable_share_pct", "missing_metric"})
    assert result["is_valid"] is False
    assert result["missing_metric_ids"] == ["missing_metric"]
