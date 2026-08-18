from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from .checkpoint import CheckpointWriter


SCHEMA = {
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


def checkpoint(checkpoint_id: str = "CP-TEST-0001") -> dict:
    return {
        "checkpoint_id": checkpoint_id,
        "timestamp": "2026-08-17T20:00:00-05:00",
        "repository_revision": "abc123",
        "active_task": "test checkpoint writer",
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


class CheckpointWriterTests(unittest.TestCase):
    def test_prepare_valid_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            writer = CheckpointWriter(repository_root=temp, schema=SCHEMA)
            plan = writer.prepare(
                checkpoint(),
                previous_checkpoint_path="context/checkpoints/CP-PREV.md",
            )
            self.assertTrue(plan.validation.valid)
            self.assertEqual(plan.checkpoint_relative_path, "context/checkpoints/CP-TEST-0001.md")
            self.assertIn('"checkpoint_id": "CP-TEST-0001"', plan.checkpoint_text)
            self.assertIn("CP-PREV.md", plan.latest_text)

    def test_invalid_checkpoint_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            writer = CheckpointWriter(repository_root=temp, schema=SCHEMA)
            value = checkpoint()
            del value["active_task"]
            with self.assertRaises(ValueError):
                writer.prepare(value)

    def test_checkpoint_id_path_traversal_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            writer = CheckpointWriter(repository_root=temp, schema=SCHEMA)
            with self.assertRaises(ValueError):
                writer.prepare(checkpoint("../escape"))

    def test_previous_checkpoint_path_must_stay_in_checkpoint_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            writer = CheckpointWriter(repository_root=temp, schema=SCHEMA)
            with self.assertRaises(ValueError):
                writer.prepare(checkpoint(), previous_checkpoint_path="../LATEST.md")

    def test_writer_is_read_only_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            writer = CheckpointWriter(repository_root=temp, schema=SCHEMA)
            plan = writer.prepare(checkpoint())
            with self.assertRaises(PermissionError):
                writer.commit(plan)

    def test_commit_creates_checkpoint_once_without_latest_update(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            writer = CheckpointWriter(repository_root=temp, schema=SCHEMA, write_enabled=True)
            plan = writer.prepare(checkpoint())
            receipt = writer.commit(plan)
            target = Path(temp) / plan.checkpoint_relative_path
            self.assertTrue(target.exists())
            self.assertFalse(receipt.latest_updated)
            with self.assertRaises(FileExistsError):
                writer.commit(plan)

    def test_latest_update_requires_compare_and_swap(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            latest = root / "context" / "LATEST.md"
            latest.parent.mkdir(parents=True)
            latest.write_text("old-pointer\n", encoding="utf-8")
            writer = CheckpointWriter(repository_root=root, schema=SCHEMA, write_enabled=True)
            plan = writer.prepare(
                checkpoint(),
                previous_checkpoint_path="context/checkpoints/CP-PREV.md",
            )
            with self.assertRaises(ValueError):
                writer.commit(plan, update_latest=True)

    def test_stale_latest_compare_and_swap_fails_before_checkpoint_write(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            latest = root / "context" / "LATEST.md"
            latest.parent.mkdir(parents=True)
            latest.write_text("newer-pointer\n", encoding="utf-8")
            writer = CheckpointWriter(repository_root=root, schema=SCHEMA, write_enabled=True)
            plan = writer.prepare(checkpoint())
            with self.assertRaises(RuntimeError):
                writer.commit(
                    plan,
                    update_latest=True,
                    expected_latest_text="stale-pointer\n",
                )
            self.assertFalse((root / plan.checkpoint_relative_path).exists())
            self.assertEqual(latest.read_text(encoding="utf-8"), "newer-pointer\n")

    def test_compare_and_swap_updates_latest_after_checkpoint_creation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            latest = root / "context" / "LATEST.md"
            latest.parent.mkdir(parents=True)
            old = "old-pointer\n"
            latest.write_text(old, encoding="utf-8")
            writer = CheckpointWriter(repository_root=root, schema=SCHEMA, write_enabled=True)
            plan = writer.prepare(
                checkpoint(),
                previous_checkpoint_path="context/checkpoints/CP-PREV.md",
            )
            receipt = writer.commit(
                plan,
                update_latest=True,
                expected_latest_text=old,
            )
            self.assertTrue(receipt.latest_updated)
            self.assertEqual(latest.read_text(encoding="utf-8"), plan.latest_text)
            self.assertTrue((root / plan.checkpoint_relative_path).exists())


if __name__ == "__main__":
    unittest.main()
