"""Reference context loader and continuity-checkpoint validator.

The core is intentionally parser-agnostic. Providers may parse YAML with their
native tooling and pass ordinary Python mappings into ``MappingRepository``.
This keeps routing, dependency resolution, and checkpoint validation testable
without making a YAML package part of the authority boundary.

The loader never executes retrieved content and never treats bundle membership,
keyword matches, or repository presence as an authority grant.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence


@dataclass(frozen=True)
class Diagnostic:
    code: str
    message: str
    severity: str = "WARNING"


@dataclass(frozen=True)
class HydrationPlan:
    task: str
    bundles: tuple[str, ...]
    records: tuple[str, ...]
    diagnostics: tuple[Diagnostic, ...]
    degraded: bool = False


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    diagnostics: tuple[Diagnostic, ...]


class MappingRepository:
    """In-memory view of already parsed continuity metadata.

    Expected keys:
      - ``context_manifest``: parsed ``context/manifest.yaml``
      - ``task_router``: parsed ``context/task-router.yaml``
      - ``bundles``: mapping of bundle ID -> parsed bundle mapping
      - ``checkpoint_schema``: parsed ``context/session-state.schema.yaml``

    This object stores metadata only. It does not fetch or execute record text.
    """

    def __init__(
        self,
        *,
        context_manifest: Mapping[str, Any],
        task_router: Mapping[str, Any],
        bundles: Mapping[str, Mapping[str, Any]],
        checkpoint_schema: Mapping[str, Any] | None = None,
    ) -> None:
        self.context_manifest = dict(context_manifest)
        self.task_router = dict(task_router)
        self.bundles = {key: dict(value) for key, value in bundles.items()}
        self.checkpoint_schema = dict(checkpoint_schema or {})


class PortableContextLoader:
    """Deterministic minimum-context planner.

    It plans which bundle IDs and repository record paths should be retrieved.
    It deliberately does not retrieve content, execute instructions, or infer
    authority from a route match.
    """

    def __init__(self, repository: MappingRepository) -> None:
        self.repository = repository

    def plan(self, task: str) -> HydrationPlan:
        manifest = self.repository.context_manifest
        router = self.repository.task_router
        diagnostics: list[Diagnostic] = []

        always = tuple(router.get("always_load", ()))
        routing_rules = router.get("routing_rules", {})
        max_initial = int(
            routing_rules.get(
                "max_initial_task_bundles",
                manifest.get("hydration_rules", {}).get("maximum_initial_task_bundles", 3),
            )
        )

        matched: list[str] = []
        normalized = task.casefold()
        for route_name, route in router.get("routes", {}).items():
            terms = route.get("match", ())
            if any(str(term).casefold() in normalized for term in terms):
                for bundle_id in route.get("bundles", ()):
                    if bundle_id not in matched:
                        matched.append(bundle_id)

        if not matched and routing_rules.get("ambiguous_task_behavior") == "CORE_ONLY_THEN_REASSESS":
            diagnostics.append(
                Diagnostic(
                    "NO_TASK_ROUTE",
                    "No task-specific route matched; CORE-only hydration is required before reassessment.",
                    "INFO",
                )
            )

        if len(matched) > max_initial:
            diagnostics.append(
                Diagnostic(
                    "TASK_BUNDLE_LIMIT_APPLIED",
                    f"Matched {len(matched)} task bundles; limited initial hydration to {max_initial}.",
                    "INFO",
                )
            )
            matched = matched[:max_initial]

        requested = list(dict.fromkeys((*always, *matched)))
        resolved: list[str] = []
        degraded = False

        for bundle_id in requested:
            ok = self._resolve_bundle(
                bundle_id,
                resolved=resolved,
                stack=(),
                diagnostics=diagnostics,
            )
            degraded = degraded or not ok

        records: list[str] = []
        for bundle_id in resolved:
            bundle = self.repository.bundles.get(bundle_id, {})
            records.extend(self._record_paths(bundle))

        return HydrationPlan(
            task=task,
            bundles=tuple(resolved),
            records=tuple(dict.fromkeys(records)),
            diagnostics=tuple(diagnostics),
            degraded=degraded,
        )

    def _resolve_bundle(
        self,
        bundle_id: str,
        *,
        resolved: list[str],
        stack: Sequence[str],
        diagnostics: list[Diagnostic],
    ) -> bool:
        if bundle_id in resolved:
            return True
        if bundle_id in stack:
            diagnostics.append(
                Diagnostic(
                    "DEPENDENCY_CYCLE",
                    "Bundle dependency cycle detected: " + " -> ".join((*stack, bundle_id)),
                    "ERROR",
                )
            )
            return False

        manifest_entry = self.repository.context_manifest.get("bundles", {}).get(bundle_id)
        if not manifest_entry:
            diagnostics.append(
                Diagnostic("BUNDLE_UNREGISTERED", f"Bundle {bundle_id!r} is not registered.", "ERROR")
            )
            return False
        if manifest_entry.get("status") != "ACTIVE":
            diagnostics.append(
                Diagnostic(
                    "BUNDLE_NOT_ACTIVE",
                    f"Bundle {bundle_id!r} is {manifest_entry.get('status', 'UNKNOWN')}; it was not hydrated.",
                    "WARNING",
                )
            )
            return False

        bundle = self.repository.bundles.get(bundle_id)
        if bundle is None:
            diagnostics.append(
                Diagnostic("BUNDLE_METADATA_MISSING", f"Parsed metadata for {bundle_id!r} is missing.", "ERROR")
            )
            return False
        if bundle.get("status") != "ACTIVE":
            diagnostics.append(
                Diagnostic(
                    "BUNDLE_METADATA_NOT_ACTIVE",
                    f"Bundle metadata for {bundle_id!r} is not ACTIVE.",
                    "ERROR",
                )
            )
            return False

        dependency_ids = list(bundle.get("requires", ()))
        # CORE uses `required` for repository paths rather than bundle dependencies.
        next_stack = (*stack, bundle_id)
        ok = True
        for dependency in dependency_ids:
            if dependency in self.repository.context_manifest.get("bundles", {}):
                ok = self._resolve_bundle(
                    str(dependency),
                    resolved=resolved,
                    stack=next_stack,
                    diagnostics=diagnostics,
                ) and ok

        if ok and bundle_id not in resolved:
            resolved.append(bundle_id)
        return ok

    @classmethod
    def _record_paths(cls, bundle: Mapping[str, Any]) -> list[str]:
        result: list[str] = []
        result.extend(cls._strings(bundle.get("required", ())))
        result.extend(cls._strings(bundle.get("records", {})))

        conditional = bundle.get("conditional", {})
        if isinstance(conditional, Mapping):
            for value in conditional.values():
                if isinstance(value, Mapping) and "selector" in value:
                    result.extend(cls._strings(value["selector"]))
        return result

    @classmethod
    def _strings(cls, value: Any) -> list[str]:
        if isinstance(value, str):
            return [value]
        if isinstance(value, Mapping):
            out: list[str] = []
            for nested in value.values():
                out.extend(cls._strings(nested))
            return out
        if isinstance(value, Iterable) and not isinstance(value, (bytes, bytearray)):
            out: list[str] = []
            for nested in value:
                out.extend(cls._strings(nested))
            return out
        return []


class CheckpointValidator:
    """Validate checkpoint mappings against the repository checkpoint schema.

    Validation is deliberately structural. It does not promote a checkpoint to
    canonical state, verify repository revisions against Git, or authorize any
    action recorded inside the checkpoint.
    """

    _TYPE_NAMES = {
        "string": str,
        "string_or_unknown": str,
        "iso8601": str,
        "list": list,
    }

    def __init__(self, schema: Mapping[str, Any]) -> None:
        self.schema = dict(schema)

    def validate(self, checkpoint: Mapping[str, Any]) -> ValidationResult:
        diagnostics: list[Diagnostic] = []
        required = self.schema.get("required_fields", {})

        for field, type_name in required.items():
            if field not in checkpoint:
                diagnostics.append(
                    Diagnostic("CHECKPOINT_FIELD_MISSING", f"Required checkpoint field {field!r} is missing.", "ERROR")
                )
                continue
            expected = self._TYPE_NAMES.get(str(type_name))
            if expected is not None and not isinstance(checkpoint[field], expected):
                diagnostics.append(
                    Diagnostic(
                        "CHECKPOINT_FIELD_TYPE",
                        f"Checkpoint field {field!r} must be {type_name}; got {type(checkpoint[field]).__name__}.",
                        "ERROR",
                    )
                )

        revision = checkpoint.get("repository_revision")
        if isinstance(revision, str) and not revision.strip():
            diagnostics.append(
                Diagnostic(
                    "CHECKPOINT_EMPTY_REVISION",
                    "repository_revision must be an exact revision or the explicit value 'unknown'.",
                    "ERROR",
                )
            )

        timestamp = checkpoint.get("timestamp")
        if isinstance(timestamp, str) and "T" not in timestamp:
            diagnostics.append(
                Diagnostic(
                    "CHECKPOINT_TIMESTAMP_FORMAT",
                    "timestamp does not resemble an ISO-8601 date-time.",
                    "ERROR",
                )
            )

        return ValidationResult(
            valid=not any(item.severity == "ERROR" for item in diagnostics),
            diagnostics=tuple(diagnostics),
        )
