from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from src.common.config import get_project_paths


class SLAPolicy(BaseModel):
    freshness_hours_max: int = Field(gt=0)
    missing_zone_records_critical: int = Field(ge=1)


class DriftPolicy(BaseModel):
    stress_index_warn: float = Field(ge=0)
    stress_index_critical: float = Field(ge=0)
    renewable_share_warn: float = Field(ge=0)
    renewable_share_critical: float = Field(ge=0)


class AlertRoutingPolicy(BaseModel):
    critical: str
    warning: str
    info: str


class BackfillPolicy(BaseModel):
    max_backfill_days: int = Field(gt=0)
    rerun_on_failure: bool
    allow_partial_backfill: bool


class Phase11Policy(BaseModel):
    sla: SLAPolicy
    drift: DriftPolicy
    alert_routing: AlertRoutingPolicy
    backfill: BackfillPolicy


def default_policy_path() -> Path:
    paths = get_project_paths()
    return paths.reference_data_dir / "monitoring" / "phase11_policy.yaml"


def load_phase11_policy(path: Path | None = None) -> Phase11Policy:
    policy_path = path or default_policy_path()

    with policy_path.open("r", encoding="utf-8") as stream:
        payload = yaml.safe_load(stream)

    return Phase11Policy.model_validate(payload)
