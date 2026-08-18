# Portable Context Loader Reference

**Status:** IMPLEMENTED / EXACT-REVISION EVIDENCE REQUIRED AFTER CHANGE

This package provides provider-neutral reference controls for repository-first continuity:

1. deterministic minimum-context bundle planning;
2. structural continuity-checkpoint validation;
3. fail-closed continuity-checkpoint preparation and local persistence.

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

For an ambiguous task under the current router policy, it returns CORE-only hydration plus a reassessment diagnostic.

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

The package includes standard-library `unittest` coverage for routing, validation, and checkpoint writing.

Run from the repository root:

```bash
python -m unittest \
  reference.context_loader.test_loader \
  reference.context_loader.test_checkpoint -v
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

No successful test claim should be attached to a changed revision until the exact revision, interpreter/runtime, command, and raw output are preserved or independently retrievable from CI.

## Next implementation step

Add the thin repository/filesystem metadata adapter that parses or accepts parsed repository metadata and feeds it into this core. Keep provider-specific retrieval and commit behavior outside the deterministic planner/writer so a provider cannot silently redefine routing, validation, or checkpoint mutation semantics.
