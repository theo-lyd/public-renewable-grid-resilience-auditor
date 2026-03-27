from pathlib import Path

from src.ingestion.contracts import load_source_inventory


def test_source_inventory_contains_core_sources() -> None:
    inventory_path = Path("data/reference/contracts/source_inventory.yaml")
    inventory = load_source_inventory(inventory_path)

    source_ids = {source.source_id for source in inventory.sources}
    assert {"entsoe_transparency", "open_meteo", "ember_electricity"}.issubset(source_ids)


def test_each_endpoint_has_required_fields_and_quality_rules() -> None:
    inventory_path = Path("data/reference/contracts/source_inventory.yaml")
    inventory = load_source_inventory(inventory_path)

    for source in inventory.sources:
        for endpoint in source.endpoints:
            assert endpoint.required_fields, f"{endpoint.endpoint_id} missing required_fields"
            assert endpoint.quality_rules, f"{endpoint.endpoint_id} missing quality_rules"
            assert endpoint.failure_modes, f"{endpoint.endpoint_id} missing failure_modes"


def test_all_endpoints_have_at_least_one_critical_quality_rule() -> None:
    inventory_path = Path("data/reference/contracts/source_inventory.yaml")
    inventory = load_source_inventory(inventory_path)

    for source in inventory.sources:
        for endpoint in source.endpoints:
            critical_rules = [
                rule for rule in endpoint.quality_rules if rule.severity == "critical"
            ]
            assert critical_rules, f"{endpoint.endpoint_id} has no critical quality rule"
