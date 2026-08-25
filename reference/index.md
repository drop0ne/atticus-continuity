# Reference Implementations

Reference code in this directory exists to turn ATTICUS/PAC hypotheses and continuity architecture into falsifiable, reproducible implementations.

## Current implementations

| ID | Component | Status | Path | Preserved result |
|---|---|---|---|---|
| `REF-PAC-GW-0001` | PAC Authority Gateway v0.2 | TESTED | `pac_gateway/` | `experiments/results/RES-2026-0001-exp0004-f3ed8958.json`; exact-revision aggregate evidence also in `reference/results/REF-CONFORMANCE-2026-0001-c4975992.json` |
| `REF-CTX-0001` | Portable Context Loader + Checkpoint Validator/Writer + Filesystem Adapter + Provider Evidence Validator | TESTED | `context_loader/` | `context/results/CTX-RES-2026-0001-f3ed8958.json`; `reference/results/REF-CONFORMANCE-2026-0001-c4975992.json` |
| `REF-SRC-INT-0001` | Source Integrity Verifier v0.1 | TESTED | `source_integrity/` | `reference/results/REF-CONFORMANCE-2026-0001-c4975992.json` |

The newest preserved combined conformance evidence applies to exact revision `c497599284e317549d3b2496383cf1b8a3c06507`: GitHub Actions run `32677079145` completed successfully under Python 3.12.3 / Ubuntu 24.04.4 with 34 continuity tests, 10 source-integrity tests, and 46 PAC gateway tests passing with zero failures/errors/skips. The workflow token exposed only `contents: read` and `metadata: read`.

`REF-SRC-INT-0001` is therefore TESTED for that exact revision. The `REF-CTX-0001` TESTED boundary now also covers the checkpoint writer, filesystem metadata adapter, and provider-conformance evidence validator present at that revision. A later change requires new exact-revision evidence before the changed implementation inherits TESTED status.

### REF-PAC-GW-0001 components

- local pre-action authority gateway;
- trusted action-intent correlation interface;
- constrained synthetic executor;
- secondary safety monitor/circuit breaker;
- tamper-evident local audit hash chain;
- aggregate plan ledger;
- multiple subject-bound local authority references per aggregate plan;
- in-process atomic budget reservation;
- conformance suites and JSON result runner.

### REF-CTX-0001 components

- parser-neutral metadata interface;
- deterministic task-to-bundle routing;
- always-load CORE behavior;
- ACTIVE-bundle enforcement;
- dependency resolution and cycle rejection;
- record-path collection without content execution;
- CORE-only ambiguous-task fallback;
- structural continuity-checkpoint validation;
- fail-closed checkpoint writer with explicit write enablement, exclusive creation, and compare-and-swap `LATEST.md` update;
- filesystem metadata adapter with path-containment and manifest/bundle consistency checks;
- provider-conformance evidence validator for CPBC result derivation;
- standard-library unit tests.

The loader returns a retrieval plan only. Bundle matches and retrieved repository records do not create truth or authority.

### REF-SRC-INT-0001 components

- deterministic chunked SHA-256 and byte-size calculation;
- single-artifact verification against expected digest and optional size;
- JSON manifest verification for multiple relative-path artifacts;
- fail-closed handling of malformed digests, missing files, duplicate paths, absolute manifest paths, and path traversal;
- machine-readable JSON result output;
- no network, execution, archive extraction, rendering, or mutation capability.

A verifier PASS proves byte agreement with the supplied expectation only. It does not establish provenance, authorship, correctness, or canonical authority.

## Status vocabulary

- `SPECIFIED` — implementation design exists but code does not.
- `IMPLEMENTED / UNEXECUTED` — code exists but repository-preserved test results do not yet exist.
- `TESTED` — tests were executed and exact results were preserved for a named revision.
- `REPLICATED` — an independent environment reproduced the tested result.
- `FAILED` — implementation did not meet preregistered criteria.
- `DEPRECATED` — retained for history, no longer the active reference.

## Rule

Code existence is not evidence of conformance.

A reference implementation may move to `TESTED` only when the exact revision, interpreter/runtime, command, output, and failures are preserved under `experiments/results/` or another explicitly indexed results path.

A later untested code change does not retroactively inherit a prior revision's TESTED status.

## Security boundary

Reference implementations must default to inert simulated resources or metadata planning. Adding real external capabilities requires a separate security review and explicit authorization; research convenience is not sufficient justification.
