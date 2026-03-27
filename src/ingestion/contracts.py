from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, field_validator

Severity = Literal["critical", "warning", "info"]
AuthType = Literal["api_key", "none"]
ResponseFormat = Literal["json", "xml", "csv"]


class RequiredField(BaseModel):
    name: str = Field(min_length=1)
    data_type: str = Field(min_length=1)
    nullable: bool
    description: str = Field(min_length=1)


class QualityRule(BaseModel):
    rule_id: str = Field(min_length=3)
    severity: Severity
    dimension: str = Field(min_length=1)
    expression: str = Field(min_length=3)


class EndpointContract(BaseModel):
    endpoint_id: str = Field(min_length=1)
    path: str = Field(min_length=1)
    method: Literal["GET", "POST"]
    response_format: ResponseFormat
    params: list[str]
    required_fields: list[RequiredField]
    quality_rules: list[QualityRule]
    failure_modes: list[str]

    @field_validator("required_fields")
    @classmethod
    def validate_required_fields_not_empty(cls, value: list[RequiredField]) -> list[RequiredField]:
        if not value:
            raise ValueError("required_fields must contain at least one field")
        return value

    @field_validator("quality_rules")
    @classmethod
    def validate_quality_rules_not_empty(cls, value: list[QualityRule]) -> list[QualityRule]:
        if not value:
            raise ValueError("quality_rules must contain at least one rule")
        return value


class SourceAuth(BaseModel):
    type: AuthType
    env_var: str
    free_tier: bool


class SourceContract(BaseModel):
    source_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    region_scope: str = Field(min_length=1)
    base_url: str = Field(min_length=1)
    auth: SourceAuth
    refresh_cadence: str = Field(min_length=1)
    reliability_tier: Literal["high", "medium", "low"]
    endpoints: list[EndpointContract]

    @field_validator("endpoints")
    @classmethod
    def validate_endpoints_not_empty(cls, value: list[EndpointContract]) -> list[EndpointContract]:
        if not value:
            raise ValueError("endpoints must contain at least one endpoint")
        return value


class SourceInventory(BaseModel):
    version: str = Field(min_length=1)
    project: str = Field(min_length=1)
    maintainer: str = Field(min_length=1)
    last_updated_utc: str = Field(min_length=1)
    sources: list[SourceContract]

    @field_validator("sources")
    @classmethod
    def validate_sources_not_empty(cls, value: list[SourceContract]) -> list[SourceContract]:
        if not value:
            raise ValueError("sources must contain at least one source contract")
        return value


def load_source_inventory(file_path: Path) -> SourceInventory:
    with file_path.open("r", encoding="utf-8") as file:
        payload = yaml.safe_load(file)

    return SourceInventory.model_validate(payload)


def get_default_inventory_path(project_root: Path | None = None) -> Path:
    root = project_root or Path(__file__).resolve().parents[2]
    return root / "data/reference/contracts/source_inventory.yaml"


def validate_default_inventory(project_root: Path | None = None) -> SourceInventory:
    inventory_path = get_default_inventory_path(project_root)
    return load_source_inventory(inventory_path)
