# Portable Context Loader Reference

**Status:** IMPLEMENTED / UNEXECUTED

This package provides a parser-neutral reference implementation for two Phase-2 continuity controls:

1. deterministic minimum-context bundle planning;
2. structural continuity-checkpoint validation.

It is intentionally inert. It does not execute retrieved repository text, contact providers, write checkpoints, modify canonical state, or infer authority from routing metadata.

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

## Tests

The package includes standard-library `unittest` cases for:

- CORE-only ambiguous routing;
- ATTICUS runtime dependency resolution;
- multi-route deduplication;
- rejection of planned bundles;
- dependency-cycle detection;
- valid checkpoint acceptance;
- missing required checkpoint fields;
- explicit revision handling.

Run from the repository root:

```bash
python -m unittest reference.context_loader.test_loader -v
```

No claim of successful execution should be made until exact revision, interpreter version, command, and raw output are preserved under `experiments/results/` or an equivalent continuity test-results path.

## Next implementation step

Add a thin provider/filesystem adapter that parses repository YAML and feeds the mappings into this core. That adapter should remain separate from the deterministic planner so provider-specific retrieval behavior cannot silently redefine routing semantics.
