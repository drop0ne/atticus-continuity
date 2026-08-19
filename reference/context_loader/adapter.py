"""Filesystem adapter for provider-neutral continuity metadata.

This module bridges repository files into ``MappingRepository`` without making
filesystem reachability, filenames, or parser output an authority source.

The adapter is intentionally parser-injected. YAML syntax support belongs to the
provider/integration edge; the deterministic continuity core consumes ordinary
Python mappings and does not depend on a third-party YAML package.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from .loader import MappingRepository


class MetadataAdapterError(ValueError):
    """Raised when continuity metadata cannot be loaded safely."""


@dataclass(frozen=True)
class MetadataSource:
    logical_name: str
    repository_path: str


@dataclass(frozen=True)
class AdapterLoadResult:
    repository: MappingRepository
    sources: tuple[MetadataSource, ...]


Parser = Callable[[str, str], Mapping[str, Any]]


class FilesystemMetadataAdapter:
    """Load parsed continuity metadata from a checked-out repository.

    Security properties:
      * read-only;
      * all resolved files must remain beneath the repository root;
      * ACTIVE bundles must have an explicit file path;
      * the parsed bundle ``id`` must match the manifest bundle ID;
      * parser output must be a mapping;
      * PLANNED/INACTIVE bundle entries are not loaded merely because files exist.

    The adapter does not validate factual correctness or canonical authority. It
    only establishes a bounded mapping between the checked-out repository layout
    and the portable loader's metadata objects.
    """

    def __init__(self, root: str | Path, *, parser: Parser) -> None:
        self.root = Path(root).resolve()
        self.context_root = (self.root / "context").resolve()
        self.parser = parser

        if not self.root.exists() or not self.root.is_dir():
            raise MetadataAdapterError("repository root does not exist or is not a directory")
        self._require_within_root(self.context_root)

    def load(self) -> AdapterLoadResult:
        sources: list[MetadataSource] = []

        manifest_path = self._resolve_repo_path("context/manifest.yaml")
        manifest = self._parse_mapping(manifest_path)
        sources.append(self._source("context_manifest", manifest_path))

        task_router_ref = self._required_string(manifest, "task_router")
        task_router_path = self._resolve_context_path(task_router_ref)
        task_router = self._parse_mapping(task_router_path)
        sources.append(self._source("task_router", task_router_path))

        schema_ref = self._required_string(manifest, "session_state_schema")
        schema_path = self._resolve_context_path(schema_ref)
        checkpoint_schema = self._parse_mapping(schema_path)
        sources.append(self._source("checkpoint_schema", schema_path))

        bundle_entries = manifest.get("bundles")
        if not isinstance(bundle_entries, Mapping):
            raise MetadataAdapterError("context manifest 'bundles' must be a mapping")

        bundles: dict[str, Mapping[str, Any]] = {}
        for raw_bundle_id, raw_entry in bundle_entries.items():
            bundle_id = str(raw_bundle_id)
            if not isinstance(raw_entry, Mapping):
                raise MetadataAdapterError(f"bundle entry {bundle_id!r} must be a mapping")

            status = str(raw_entry.get("status", "UNKNOWN"))
            if status != "ACTIVE":
                continue

            file_ref = raw_entry.get("file")
            if not isinstance(file_ref, str) or not file_ref.strip():
                raise MetadataAdapterError(
                    f"ACTIVE bundle {bundle_id!r} must declare a non-empty file path"
                )

            bundle_path = self._resolve_context_path(file_ref)
            bundle = self._parse_mapping(bundle_path)
            parsed_id = bundle.get("id")
            if parsed_id != bundle_id:
                raise MetadataAdapterError(
                    f"bundle ID mismatch for {bundle_id!r}: parsed id is {parsed_id!r}"
                )
            if bundle.get("status") != "ACTIVE":
                raise MetadataAdapterError(
                    f"manifest marks {bundle_id!r} ACTIVE but bundle metadata is not ACTIVE"
                )

            bundles[bundle_id] = bundle
            sources.append(self._source(f"bundle:{bundle_id}", bundle_path))

        repository = MappingRepository(
            context_manifest=manifest,
            task_router=task_router,
            bundles=bundles,
            checkpoint_schema=checkpoint_schema,
        )
        return AdapterLoadResult(repository=repository, sources=tuple(sources))

    def _parse_mapping(self, path: Path) -> Mapping[str, Any]:
        if not path.exists() or not path.is_file():
            raise MetadataAdapterError(f"required metadata file is missing: {self._relative(path)}")
        text = path.read_text(encoding="utf-8")
        parsed = self.parser(text, self._relative(path))
        if not isinstance(parsed, Mapping):
            raise MetadataAdapterError(
                f"parser returned non-mapping metadata for {self._relative(path)}"
            )
        return dict(parsed)

    def _resolve_context_path(self, relative: str) -> Path:
        candidate = (self.context_root / relative).resolve()
        self._require_within_root(candidate)
        return candidate

    def _resolve_repo_path(self, relative: str) -> Path:
        candidate = (self.root / relative).resolve()
        self._require_within_root(candidate)
        return candidate

    def _require_within_root(self, path: Path) -> None:
        try:
            path.relative_to(self.root)
        except ValueError as exc:
            raise MetadataAdapterError(
                f"metadata path escapes repository root: {path}"
            ) from exc

    def _relative(self, path: Path) -> str:
        self._require_within_root(path)
        return path.relative_to(self.root).as_posix()

    def _source(self, logical_name: str, path: Path) -> MetadataSource:
        return MetadataSource(logical_name=logical_name, repository_path=self._relative(path))

    @staticmethod
    def _required_string(mapping: Mapping[str, Any], key: str) -> str:
        value = mapping.get(key)
        if not isinstance(value, str) or not value.strip():
            raise MetadataAdapterError(f"context manifest {key!r} must be a non-empty string")
        return value
