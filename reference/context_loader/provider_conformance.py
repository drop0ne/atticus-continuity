"""Provider-neutral continuity conformance result validation.

This module validates evidence records only. It does not contact providers,
execute models, or grant repository authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Sequence


REQUIRED_SCENARIOS: tuple[str, ...] = tuple(f"CPBC-{i:02d}" for i in range(1, 13))


class ScenarioStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    NOT_RUN = "NOT_RUN"


class OverallStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    INCOMPLETE = "INCOMPLETE"


@dataclass(frozen=True)
class ScenarioResult:
    status: ScenarioStatus
    evidence: str = ""
    notes: str = ""


@dataclass(frozen=True)
class ProviderConformanceRecord:
    result_id: str
    timestamp: str
    repository_revision: str
    adapter_id: str
    provider_family: str
    runtime_or_model: str
    adapter_revision_or_file: str
    environment: str
    capabilities: Mapping[str, str]
    scenarios: Mapping[str, ScenarioResult]
    overall_status: OverallStatus
    limitations: Sequence[str] = ()


class ConformanceValidationError(ValueError):
    """Raised when a conformance evidence record is structurally invalid."""


def derive_overall_status(scenarios: Mapping[str, ScenarioResult]) -> OverallStatus:
    """Derive status from the fixed twelve-scenario contract."""
    required = [scenarios.get(scenario_id) for scenario_id in REQUIRED_SCENARIOS]
    if any(item is not None and item.status == ScenarioStatus.FAIL for item in required):
        return OverallStatus.FAIL
    if any(item is None or item.status != ScenarioStatus.PASS for item in required):
        return OverallStatus.INCOMPLETE
    return OverallStatus.PASS


def validate_conformance_record(record: ProviderConformanceRecord) -> tuple[str, ...]:
    """Return validation warnings or raise on evidence-integrity violations."""
    required_text = {
        "result_id": record.result_id,
        "timestamp": record.timestamp,
        "repository_revision": record.repository_revision,
        "adapter_id": record.adapter_id,
        "provider_family": record.provider_family,
        "runtime_or_model": record.runtime_or_model,
        "adapter_revision_or_file": record.adapter_revision_or_file,
        "environment": record.environment,
    }
    missing = [name for name, value in required_text.items() if not str(value).strip()]
    if missing:
        raise ConformanceValidationError(
            "missing required identity fields: " + ", ".join(sorted(missing))
        )

    unknown_scenarios = sorted(set(record.scenarios) - set(REQUIRED_SCENARIOS))
    if unknown_scenarios:
        raise ConformanceValidationError(
            "unknown scenario ids: " + ", ".join(unknown_scenarios)
        )

    derived = derive_overall_status(record.scenarios)
    if record.overall_status != derived:
        raise ConformanceValidationError(
            f"overall_status mismatch: declared={record.overall_status.value} "
            f"derived={derived.value}"
        )

    warnings: list[str] = []
    missing_scenarios = [sid for sid in REQUIRED_SCENARIOS if sid not in record.scenarios]
    if missing_scenarios:
        warnings.append("missing scenarios: " + ", ".join(missing_scenarios))

    for scenario_id, result in record.scenarios.items():
        if result.status == ScenarioStatus.PASS and not result.evidence.strip():
            warnings.append(f"{scenario_id} PASS has no evidence text")
        if result.status == ScenarioStatus.BLOCKED and not result.notes.strip():
            warnings.append(f"{scenario_id} BLOCKED has no blocking note")

    if record.overall_status == OverallStatus.PASS and record.limitations:
        warnings.append("PASS record contains limitations; review scope before reuse")

    return tuple(warnings)
