from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from .adapter import FilesystemMetadataAdapter, MetadataAdapterError
from .loader import PortableContextLoader


def json_parser(text: str, source: str):
    _ = source
    return json.loads(text)


class FilesystemMetadataAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "context" / "bundles").mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_json(self, relative: str, value) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")

    def build_valid_tree(self) -> None:
        self.write_json(
            "context/manifest.yaml",
            {
                "task_router": "task-router.yaml",
                "session_state_schema": "session-state.schema.yaml",
                "bundles": {
                    "CORE": {"file": "bundles/CORE.yaml", "status": "ACTIVE"},
                    "ATTICUS_RUNTIME": {
                        "file": "bundles/ATTICUS_RUNTIME.yaml",
                        "status": "ACTIVE",
                    },
                    "PLANNED": {"status": "PLANNED"},
                },
            },
        )
        self.write_json(
            "context/task-router.yaml",
            {
                "always_load": ["CORE"],
                "routing_rules": {
                    "ambiguous_task_behavior": "CORE_ONLY_THEN_REASSESS",
                    "max_initial_task_bundles": 3,
                },
                "routes": {
                    "atticus": {
                        "match": ["atticus"],
                        "bundles": ["ATTICUS_RUNTIME"],
                    }
                },
            },
        )
        self.write_json(
            "context/session-state.schema.yaml",
            {"required_fields": {"checkpoint_id": "string"}},
        )
        self.write_json(
            "context/bundles/CORE.yaml",
            {
                "id": "CORE",
                "status": "ACTIVE",
                "required": ["PORTABLE_BOOTSTRAP.md"],
            },
        )
        self.write_json(
            "context/bundles/ATTICUS_RUNTIME.yaml",
            {
                "id": "ATTICUS_RUNTIME",
                "status": "ACTIVE",
                "requires": ["CORE"],
                "records": {"runtime": ["atticus/canonical/current.md"]},
            },
        )

    def test_loads_active_metadata_and_skips_planned_bundle(self) -> None:
        self.build_valid_tree()
        result = FilesystemMetadataAdapter(self.root, parser=json_parser).load()
        self.assertEqual(set(result.repository.bundles), {"CORE", "ATTICUS_RUNTIME"})
        self.assertEqual(
            [source.repository_path for source in result.sources],
            [
                "context/manifest.yaml",
                "context/task-router.yaml",
                "context/session-state.schema.yaml",
                "context/bundles/CORE.yaml",
                "context/bundles/ATTICUS_RUNTIME.yaml",
            ],
        )

    def test_loaded_repository_is_consumable_by_portable_loader(self) -> None:
        self.build_valid_tree()
        repository = FilesystemMetadataAdapter(self.root, parser=json_parser).load().repository
        plan = PortableContextLoader(repository).plan("continue ATTICUS runtime work")
        self.assertFalse(plan.degraded)
        self.assertEqual(plan.bundles, ("CORE", "ATTICUS_RUNTIME"))
        self.assertIn("PORTABLE_BOOTSTRAP.md", plan.records)
        self.assertIn("atticus/canonical/current.md", plan.records)

    def test_rejects_path_escape_from_context_manifest(self) -> None:
        self.build_valid_tree()
        manifest = json.loads((self.root / "context/manifest.yaml").read_text(encoding="utf-8"))
        manifest["task_router"] = "../../outside.yaml"
        self.write_json("context/manifest.yaml", manifest)
        with self.assertRaises(MetadataAdapterError):
            FilesystemMetadataAdapter(self.root, parser=json_parser).load()

    def test_rejects_absolute_path_escape(self) -> None:
        self.build_valid_tree()
        manifest = json.loads((self.root / "context/manifest.yaml").read_text(encoding="utf-8"))
        manifest["session_state_schema"] = "/tmp/schema.yaml"
        self.write_json("context/manifest.yaml", manifest)
        with self.assertRaises(MetadataAdapterError):
            FilesystemMetadataAdapter(self.root, parser=json_parser).load()

    def test_active_bundle_requires_explicit_file(self) -> None:
        self.build_valid_tree()
        manifest = json.loads((self.root / "context/manifest.yaml").read_text(encoding="utf-8"))
        manifest["bundles"]["BROKEN"] = {"status": "ACTIVE"}
        self.write_json("context/manifest.yaml", manifest)
        with self.assertRaises(MetadataAdapterError):
            FilesystemMetadataAdapter(self.root, parser=json_parser).load()

    def test_rejects_bundle_id_mismatch(self) -> None:
        self.build_valid_tree()
        self.write_json(
            "context/bundles/ATTICUS_RUNTIME.yaml",
            {"id": "OTHER", "status": "ACTIVE", "requires": ["CORE"]},
        )
        with self.assertRaises(MetadataAdapterError):
            FilesystemMetadataAdapter(self.root, parser=json_parser).load()

    def test_rejects_manifest_bundle_status_disagreement(self) -> None:
        self.build_valid_tree()
        self.write_json(
            "context/bundles/ATTICUS_RUNTIME.yaml",
            {"id": "ATTICUS_RUNTIME", "status": "INACTIVE"},
        )
        with self.assertRaises(MetadataAdapterError):
            FilesystemMetadataAdapter(self.root, parser=json_parser).load()

    def test_missing_required_metadata_file_fails_closed(self) -> None:
        self.build_valid_tree()
        (self.root / "context/task-router.yaml").unlink()
        with self.assertRaises(MetadataAdapterError):
            FilesystemMetadataAdapter(self.root, parser=json_parser).load()

    def test_parser_must_return_mapping(self) -> None:
        self.build_valid_tree()

        def bad_parser(text: str, source: str):
            _ = text, source
            return ["not", "a", "mapping"]

        with self.assertRaises(MetadataAdapterError):
            FilesystemMetadataAdapter(self.root, parser=bad_parser).load()


if __name__ == "__main__":
    unittest.main()
