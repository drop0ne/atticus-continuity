from __future__ import annotations

import unittest

from .loader import CheckpointValidator, MappingRepository, PortableContextLoader


CONTEXT_MANIFEST = {
    "bundles": {
        "CORE": {"file": "bundles/CORE.yaml", "status": "ACTIVE"},
        "ATTICUS_RUNTIME": {"file": "bundles/ATTICUS_RUNTIME.yaml", "status": "ACTIVE"},
        "PAC_GOVERNANCE": {"file": "bundles/PAC_GOVERNANCE.yaml", "status": "ACTIVE"},
        "PLANNED": {"status": "PLANNED"},
    },
    "hydration_rules": {"maximum_initial_task_bundles": 3},
}

TASK_ROUTER = {
    "always_load": ["CORE"],
    "routes": {
        "atticus": {"match": ["atticus", "runtime"], "bundles": ["ATTICUS_RUNTIME"]},
        "pac": {"match": ["pac", "governance"], "bundles": ["PAC_GOVERNANCE"]},
        "planned": {"match": ["future-only"], "bundles": ["PLANNED"]},
    },
    "routing_rules": {
        "max_initial_task_bundles": 3,
        "ambiguous_task_behavior": "CORE_ONLY_THEN_REASSESS",
    },
}

BUNDLES = {
    "CORE": {
        "id": "CORE",
        "status": "ACTIVE",
        "required": ["README.md", "manifest.yaml"],
        "conditional": {"checkpoint": {"selector": "context/LATEST.md"}},
    },
    "ATTICUS_RUNTIME": {
        "id": "ATTICUS_RUNTIME",
        "status": "ACTIVE",
        "requires": ["CORE"],
        "records": {"canonical": ["atticus/canonical/current.md"], "source": ["atticus/source/map.yaml"]},
    },
    "PAC_GOVERNANCE": {
        "id": "PAC_GOVERNANCE",
        "status": "ACTIVE",
        "requires": ["CORE"],
        "records": {"principles": ["pac/principles/PAC_BASELINE.md"]},
    },
}

CHECKPOINT_SCHEMA = {
    "required_fields": {
        "checkpoint_id": "string",
        "timestamp": "iso8601",
        "repository_revision": "string_or_unknown",
        "active_task": "string",
        "status": "string",
        "decisions": "list",
        "open_questions": "list",
        "files_changed": "list",
        "active_context_bundles": "list",
        "evidence_added": "list",
        "experiments_changed": "list",
        "next_actions": "list",
        "blocking_unknowns": "list",
    }
}


def repo(**overrides):
    values = {
        "context_manifest": CONTEXT_MANIFEST,
        "task_router": TASK_ROUTER,
        "bundles": BUNDLES,
        "checkpoint_schema": CHECKPOINT_SCHEMA,
    }
    values.update(overrides)
    return MappingRepository(**values)


class PortableContextLoaderTests(unittest.TestCase):
    def test_ambiguous_task_loads_core_only(self) -> None:
        plan = PortableContextLoader(repo()).plan("write a neutral paragraph")
        self.assertEqual(plan.bundles, ("CORE",))
        self.assertIn("README.md", plan.records)
        self.assertTrue(any(d.code == "NO_TASK_ROUTE" for d in plan.diagnostics))
        self.assertFalse(plan.degraded)

    def test_atticus_route_resolves_core_dependency_first(self) -> None:
        plan = PortableContextLoader(repo()).plan("inspect ATTICUS runtime modules")
        self.assertEqual(plan.bundles, ("CORE", "ATTICUS_RUNTIME"))
        self.assertIn("atticus/canonical/current.md", plan.records)
        self.assertIn("context/LATEST.md", plan.records)
        self.assertFalse(plan.degraded)

    def test_multiple_routes_deduplicate_core_and_records(self) -> None:
        plan = PortableContextLoader(repo()).plan("ATTICUS PAC governance runtime")
        self.assertEqual(plan.bundles, ("CORE", "ATTICUS_RUNTIME", "PAC_GOVERNANCE"))
        self.assertEqual(plan.records.count("README.md"), 1)

    def test_planned_bundle_is_not_hydrated(self) -> None:
        plan = PortableContextLoader(repo()).plan("future-only feature")
        self.assertEqual(plan.bundles, ("CORE",))
        self.assertTrue(plan.degraded)
        self.assertTrue(any(d.code == "BUNDLE_NOT_ACTIVE" for d in plan.diagnostics))

    def test_dependency_cycle_stops_and_reports(self) -> None:
        bundles = dict(BUNDLES)
        bundles["CORE"] = dict(BUNDLES["CORE"], requires=["ATTICUS_RUNTIME"])
        plan = PortableContextLoader(repo(bundles=bundles)).plan("ATTICUS runtime")
        self.assertTrue(plan.degraded)
        self.assertTrue(any(d.code == "DEPENDENCY_CYCLE" for d in plan.diagnostics))


class CheckpointValidatorTests(unittest.TestCase):
    def valid_checkpoint(self):
        return {
            "checkpoint_id": "CP-TEST",
            "timestamp": "2026-08-15T20:00:00-05:00",
            "repository_revision": "unknown",
            "active_task": "test",
            "status": "COMPLETE",
            "decisions": [],
            "open_questions": [],
            "files_changed": [],
            "active_context_bundles": ["CORE"],
            "evidence_added": [],
            "experiments_changed": [],
            "next_actions": [],
            "blocking_unknowns": [],
        }

    def test_valid_checkpoint_passes(self) -> None:
        result = CheckpointValidator(CHECKPOINT_SCHEMA).validate(self.valid_checkpoint())
        self.assertTrue(result.valid)
        self.assertEqual(result.diagnostics, ())

    def test_missing_required_field_fails(self) -> None:
        checkpoint = self.valid_checkpoint()
        del checkpoint["status"]
        result = CheckpointValidator(CHECKPOINT_SCHEMA).validate(checkpoint)
        self.assertFalse(result.valid)
        self.assertTrue(any(d.code == "CHECKPOINT_FIELD_MISSING" for d in result.diagnostics))

    def test_empty_revision_fails_but_unknown_is_allowed(self) -> None:
        checkpoint = self.valid_checkpoint()
        checkpoint["repository_revision"] = ""
        result = CheckpointValidator(CHECKPOINT_SCHEMA).validate(checkpoint)
        self.assertFalse(result.valid)
        self.assertTrue(any(d.code == "CHECKPOINT_EMPTY_REVISION" for d in result.diagnostics))


if __name__ == "__main__":
    unittest.main()
