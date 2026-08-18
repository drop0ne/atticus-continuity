"""Fail-closed continuity-checkpoint writer for repository-first handoff.

This module is deliberately local and provider-neutral. It validates an already
constructed checkpoint mapping, prepares deterministic Markdown, and can write
that checkpoint to a caller-supplied repository root only when write authority is
explicitly enabled.

It does not:
- infer or verify Git revisions;
- promote checkpoint statements to canonical state;
- execute checkpoint content;
- contact a provider or Git hosting service;
- overwrite an existing checkpoint;
- update ``context/LATEST.md`` without an explicit compare-and-swap precondition.
"""

from __future__ import annotations

import json
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional

from .loader import CheckpointValidator, ValidationResult


_CHECKPOINT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,199}$")


@dataclass(frozen=True)
class CheckpointWritePlan:
    checkpoint_id: str
    checkpoint_relative_path: str
    latest_relative_path: str
    checkpoint_text: str
    latest_text: str
    previous_checkpoint_path: Optional[str]
    validation: ValidationResult


@dataclass(frozen=True)
class CheckpointWriteReceipt:
    checkpoint_relative_path: str
    latest_updated: bool


class CheckpointWriter:
    """Prepare and optionally persist validated continuity checkpoints.

    ``write_enabled`` defaults to ``False``. A provider or local orchestration
    layer must opt in explicitly before any filesystem mutation is possible.
    """

    def __init__(
        self,
        *,
        repository_root: str | Path,
        schema: Mapping[str, Any],
        write_enabled: bool = False,
    ) -> None:
        self.repository_root = Path(repository_root).resolve()
        self.validator = CheckpointValidator(schema)
        self.write_enabled = write_enabled

    def prepare(
        self,
        checkpoint: Mapping[str, Any],
        *,
        previous_checkpoint_path: str | None = None,
    ) -> CheckpointWritePlan:
        validation = self.validator.validate(checkpoint)
        if not validation.valid:
            codes = ", ".join(item.code for item in validation.diagnostics)
            raise ValueError(f"checkpoint validation failed: {codes}")

        checkpoint_id = str(checkpoint.get("checkpoint_id", ""))
        if not _CHECKPOINT_ID.fullmatch(checkpoint_id):
            raise ValueError("checkpoint_id is not a safe repository filename component")

        checkpoint_relative_path = f"context/checkpoints/{checkpoint_id}.md"
        latest_relative_path = "context/LATEST.md"

        previous = self._normalize_previous(previous_checkpoint_path)
        checkpoint_text = self.render_checkpoint(checkpoint)
        latest_text = self.render_latest_pointer(
            checkpoint_relative_path,
            previous_checkpoint_path=previous,
        )

        return CheckpointWritePlan(
            checkpoint_id=checkpoint_id,
            checkpoint_relative_path=checkpoint_relative_path,
            latest_relative_path=latest_relative_path,
            checkpoint_text=checkpoint_text,
            latest_text=latest_text,
            previous_checkpoint_path=previous,
            validation=validation,
        )

    @staticmethod
    def render_checkpoint(checkpoint: Mapping[str, Any]) -> str:
        """Render a deterministic Markdown checkpoint with a JSON payload.

        JSON is used for the machine-readable payload because the standard
        library can serialize it deterministically and every JSON document is
        also valid YAML 1.2. Human-readable handoff text is kept outside the
        payload so it cannot silently change the structured state.
        """
        checkpoint_id = str(checkpoint["checkpoint_id"])
        payload = json.dumps(dict(checkpoint), indent=2, ensure_ascii=False)
        return (
            f"# {checkpoint_id}\n\n"
            "```json\n"
            f"{payload}\n"
            "```\n\n"
            "## Handoff\n\n"
            "This checkpoint is continuity metadata only. It does not confer canonical authority, "
            "prove completion, or authorize future actions. Resolve canonical state from the repository "
            "manifest and verify material claims before acting on them.\n"
        )

    @staticmethod
    def render_latest_pointer(
        checkpoint_relative_path: str,
        *,
        previous_checkpoint_path: str | None = None,
    ) -> str:
        text = (
            "# Latest General Continuity Checkpoint\n\n"
            "Current checkpoint:\n\n"
            f"`{checkpoint_relative_path}`\n\n"
            "A fresh session should read `PORTABLE_BOOTSTRAP.md` first, resolve the repository manifest "
            "and canonical state, load `CORE`, then follow this pointer.\n"
        )
        if previous_checkpoint_path:
            text += f"\nPrevious checkpoint:\n\n`{previous_checkpoint_path}`\n"
        text += (
            "\nThis pointer is convenience metadata. It does not itself confer canonical authority.\n"
        )
        return text

    def commit(
        self,
        plan: CheckpointWritePlan,
        *,
        update_latest: bool = False,
        expected_latest_text: str | None = None,
    ) -> CheckpointWriteReceipt:
        """Commit a prepared checkpoint with fail-closed mutation semantics.

        Existing checkpoint files are never overwritten. ``LATEST.md`` may be
        changed only when ``update_latest=True`` and the caller supplies the
        exact current text as a compare-and-swap precondition. This prevents a
        stale writer from silently replacing a newer continuity pointer.
        """
        if not self.write_enabled:
            raise PermissionError("checkpoint writer is read-only; enable writes explicitly")
        if not plan.validation.valid:
            raise ValueError("cannot commit an invalid checkpoint plan")

        checkpoint_path = self._resolve_inside_root(plan.checkpoint_relative_path)
        latest_path = self._resolve_inside_root(plan.latest_relative_path)

        if checkpoint_path.exists():
            raise FileExistsError(f"checkpoint already exists: {plan.checkpoint_relative_path}")

        if update_latest:
            if expected_latest_text is None:
                raise ValueError("LATEST update requires expected_latest_text compare-and-swap precondition")
            if not latest_path.exists():
                raise FileNotFoundError(plan.latest_relative_path)
            current_latest = latest_path.read_text(encoding="utf-8")
            if current_latest != expected_latest_text:
                raise RuntimeError("LATEST compare-and-swap failed; repository state changed")

        checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        self._exclusive_write(checkpoint_path, plan.checkpoint_text)

        latest_updated = False
        try:
            if update_latest:
                self._atomic_replace(latest_path, plan.latest_text)
                latest_updated = True
        except BaseException:
            # The checkpoint itself is durable evidence and is therefore not
            # deleted if pointer update fails. A caller can retry only the
            # pointer update after inspecting repository state.
            raise

        return CheckpointWriteReceipt(
            checkpoint_relative_path=plan.checkpoint_relative_path,
            latest_updated=latest_updated,
        )

    def _resolve_inside_root(self, relative_path: str) -> Path:
        candidate = (self.repository_root / relative_path).resolve()
        try:
            candidate.relative_to(self.repository_root)
        except ValueError as exc:
            raise ValueError("path escapes repository root") from exc
        return candidate

    @staticmethod
    def _normalize_previous(previous_checkpoint_path: str | None) -> str | None:
        if previous_checkpoint_path is None:
            return None
        previous = previous_checkpoint_path.strip().replace("\\", "/")
        if not previous.startswith("context/checkpoints/") or ".." in previous.split("/"):
            raise ValueError("previous checkpoint path must stay under context/checkpoints/")
        return previous

    @staticmethod
    def _exclusive_write(path: Path, text: str) -> None:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())

    @staticmethod
    def _atomic_replace(path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        temp_path = Path(temp_name)
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_path, path)
        finally:
            if temp_path.exists():
                temp_path.unlink()
