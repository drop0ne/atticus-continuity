from __future__ import annotations

import unittest

from .provider_conformance import (
    ConformanceValidationError,
    OverallStatus,
    ProviderConformanceRecord,
    ScenarioResult,
    ScenarioStatus,
    derive_overall_status,
    validate_conformance_record,
)


def make_record(*, statuses=None, overall=OverallStatus.PASS, limitations=()):
    statuses = statuses or {f"CPBC-{i:02d}": ScenarioStatus.PASS for i in range(1, 13)}
    scenarios = {
        scenario_id: ScenarioResult(status=status, evidence="observed evidence", notes="")
        for scenario_id, status in statuses.items()
    }
    return ProviderConformanceRecord(
        result_id="CPBC-RES-TEST-1",
        timestamp="2026-08-21T00:00:00Z",
        repository_revision="deadbeef",
        adapter_id="test-adapter",
        provider_family="test-provider",
        runtime_or_model="test-runtime",
        adapter_revision_or_file="context/provider-adapters/test.md",
        environment="unit-test",
        capabilities={"repository_read": "SUPPORTED"},
        scenarios=scenarios,
        overall_status=overall,
        limitations=limitations,
    )


class ProviderConformanceTests(unittest.TestCase):
    def test_all_required_pass_derives_pass(self) -> None:
        record = make_record()
        self.assertEqual(derive_overall_status(record.scenarios), OverallStatus.PASS)
        self.assertEqual(validate_conformance_record(record), ())

    def test_any_failure_derives_fail(self) -> None:
        statuses = {f"CPBC-{i:02d}": ScenarioStatus.PASS for i in range(1, 13)}
        statuses["CPBC-07"] = ScenarioStatus.FAIL
        self.assertEqual(
            derive_overall_status(make_record(statuses=statuses, overall=OverallStatus.FAIL).scenarios),
            OverallStatus.FAIL,
        )

    def test_blocked_without_fail_is_incomplete(self) -> None:
        statuses = {f"CPBC-{i:02d}": ScenarioStatus.PASS for i in range(1, 13)}
        statuses["CPBC-09"] = ScenarioStatus.BLOCKED
        record = make_record(statuses=statuses, overall=OverallStatus.INCOMPLETE)
        self.assertEqual(derive_overall_status(record.scenarios), OverallStatus.INCOMPLETE)

    def test_missing_scenario_is_incomplete(self) -> None:
        statuses = {f"CPBC-{i:02d}": ScenarioStatus.PASS for i in range(1, 12)}
        record = make_record(statuses=statuses, overall=OverallStatus.INCOMPLETE)
        warnings = validate_conformance_record(record)
        self.assertTrue(any("CPBC-12" in warning for warning in warnings))

    def test_declared_pass_cannot_hide_failure(self) -> None:
        statuses = {f"CPBC-{i:02d}": ScenarioStatus.PASS for i in range(1, 13)}
        statuses["CPBC-03"] = ScenarioStatus.FAIL
        with self.assertRaises(ConformanceValidationError):
            validate_conformance_record(make_record(statuses=statuses, overall=OverallStatus.PASS))

    def test_unknown_scenario_rejected(self) -> None:
        statuses = {f"CPBC-{i:02d}": ScenarioStatus.PASS for i in range(1, 13)}
        statuses["CPBC-99"] = ScenarioStatus.PASS
        with self.assertRaises(ConformanceValidationError):
            validate_conformance_record(make_record(statuses=statuses, overall=OverallStatus.PASS))

    def test_missing_identity_rejected(self) -> None:
        record = make_record()
        broken = ProviderConformanceRecord(
            **{**record.__dict__, "repository_revision": ""}
        )
        with self.assertRaises(ConformanceValidationError):
            validate_conformance_record(broken)

    def test_pass_without_evidence_warns(self) -> None:
        record = make_record()
        scenarios = dict(record.scenarios)
        scenarios["CPBC-01"] = ScenarioResult(ScenarioStatus.PASS, evidence="")
        changed = ProviderConformanceRecord(**{**record.__dict__, "scenarios": scenarios})
        warnings = validate_conformance_record(changed)
        self.assertTrue(any("CPBC-01 PASS has no evidence" in warning for warning in warnings))


if __name__ == "__main__":
    unittest.main()
