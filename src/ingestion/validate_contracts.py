from __future__ import annotations

from src.ingestion.contracts import validate_default_inventory


def run_contract_validation() -> str:
    inventory = validate_default_inventory()

    source_count = len(inventory.sources)
    endpoint_count = sum(len(source.endpoints) for source in inventory.sources)
    rule_count = sum(
        len(endpoint.quality_rules) for source in inventory.sources for endpoint in source.endpoints
    )

    return (
        "Phase 3 contract validation passed: "
        f"{source_count} sources, {endpoint_count} endpoints, {rule_count} quality rules."
    )


if __name__ == "__main__":
    print(run_contract_validation())
