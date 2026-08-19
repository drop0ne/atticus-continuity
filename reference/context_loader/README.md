# Portable Context Loader Reference

**Status:** IMPLEMENTED / EXACT-REVISION EVIDENCE REQUIRED AFTER CHANGE

This package provides provider-neutral reference controls for repository-first continuity:

1. deterministic minimum-context bundle planning;
2. structural continuity-checkpoint validation;
3. fail-closed continuity-checkpoint preparation and local persistence;
4. a read-only filesystem metadata adapter for checked-out repositories.

The routing core remains inert: it does not execute retrieved repository text, contact providers, modify canonical state, or infer authority from routing metadata. The checkpoint writer is read-only by default and requires explicit write enablement before any filesystem mutation.

## Design boundary

The core accepts already parsed mappings rather than making a YAML parser part of the governance boundary.

A provider adapter may parse:

- `context/manifest.yaml`
- `context/task-router.yaml`
- active files under `context/bundles/`
- `context/session-state.schema.yaml`

and pass those mappings into `MappingRepository`.

This allows providers with different native tooling to share the same routing and validation semantics.

## Filesystem metadata adapter

`FilesystemMetadataAdapter` bridges an ordinary checked-out repository into `MappingRepository` while keeping parsing provider-neutral through an injected `parser(text, source)` callable.

It is read-only and fail-closed. It:

- requires every resolved metadata path to remain beneath the repository root;
- loads only bundles marked `ACTIVE` by the context manifest;
- requires each active bundle to have an explicit file path;
- requires the parsed bundle `id` to match the manifest bundle ID;
- requires the bundle metadata itself to remain `ACTIVE`;
- rejects missing required files and non-mapping parser results;
- returns a source ledger recording the exact repository paths used to construct the in-memory metadata view.

It does **not** make filesystem reachability, parser output, filename recency, or manifest presence canonical authority. Canonical resolution remains governed by `PORTABLE_BOOTSTRAP.md` and the repository's controlling manifest records.

## Hydration relation

```text
operator task
    -> route match
    -> always-load CORE
    -> resolve ACTIVE bundle dependencies
    -> reject planned/missing/cyclic bundle state
    -> collect repository record paths
    -> return HydrationPlan
```

The returned plan is a retrieval plan only.

```text
route match != truth
route match != authority
bundle membership != authority
repository presence != truth
```

## Fail behavior

The reference implementation reports and degrades when:

- a requested bundle is unregistered;
- a bundle is not `ACTIVE`;
- parsed bundle metadata is missing;
- a dependency cycle is detected.

The filesystem adapter instead raises a deterministic `MetadataAdapterError` when required continuity metadata cannot be mapped safely into the core.

For an ambiguous task under the current router policy, the loader returns CORE-only hydration plus a reassessment diagnostic.

## Checkpoint validation

`CheckpointValidator` checks the required fields and structural types declared in `context/session-state.schema.yaml`.

It does **not**:

- verify a Git revision exists;
- verify that changed files actually changed;
- make checkpoint statements canonical;
- authorize actions described by the checkpoint;
- verify source citations.

Those are separate controls.

## Checkpoint writer

`CheckpointWriter` converts a validated checkpoint mapping into deterministic Markdown containing a machine-readable JSON payload.

JSON is used deliberately because it can be serialized deterministically with the Python standard library and is also valid YAML 1.2. The writer does not depend on a YAML package.

Mutation rules:

- `write_enabled=False` by default;
- invalid checkpoints cannot be prepared for write;
- unsafe checkpoint IDs and path traversal are rejected;
- existing checkpoint files are never overwritten;
- `context/LATEST.md` is not updated unless explicitly requested;
- a `LATEST.md` update requires the caller to supply the exact current text as a compare-and-swap precondition;
- stale writers fail before creating a checkpoint when the pointer precondition no longer matches;
- checkpoint contents remain continuity metadata and do not confer canonical authority.

Reference sequence:

```text
checkpoint mapping
    -> CheckpointValidator
    -> prepare CheckpointWritePlan
    -> explicit write enablement
    -> exclusive checkpoint create
    -> optional compare-and-swap LATEST update
    -> CheckpointWriteReceipt
```

The local writer is not a GitHub commit adapter. Provider-specific repository commit semantics remain a separate layer.

## Tests

The package includes standard-library `unittest` coverage for routing, validation, checkpoint writing, and filesystem metadata mapping.

Run from the repository root:

```bash
python -m unittest \
  reference.context_loader.test_loader \
  reference.context_loader.test_checkpoint \
  reference.context_loader.test_adapter -v
```

Checkpoint-writer tests cover:

- valid plan preparation;
- missing required fields;
- path traversal rejection;
- read-only default behavior;
- exclusive create / no overwrite;
- compare-and-swap requirement for `LATEST.md`;
- stale-pointer rejection before checkpoint creation;
- successful explicit pointer update.

Filesystem-adapter tests cover:

- loading active bundle metadata;
- excluding planned bundles;
- end-to-end handoff into `PortableContextLoader`;
- relative and absolute path escape rejection;
- missing active-bundle file declarations;
- bundle-ID mismatch;
- manifest/bundle status disagreement;
- missing required metadata files;
- non-mapping parser output.

No successful test claim should be attached to a changed revision until the exact revision, interpreter/runtime, command, and raw output are preserved or independently retrievable from CI.

## Next implementation step

Add the provider-adapter template that standardizes repository retrieval, parser integration, hydration-plan retrieval, capability reporting, and checkpoint handoff without allowing a provider to redefine the deterministic planner or writer semantics.
