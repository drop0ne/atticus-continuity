# Reference Implementations

Reference code in this directory exists to turn ATTICUS/PAC hypotheses and continuity architecture into falsifiable, reproducible implementations.

## Current implementations

| ID | Component | Status | Path |
|---|---|---|---|
| `REF-PAC-GW-0001` | PAC Authority Gateway v0.2 | IMPLEMENTED / UNEXECUTED | `pac_gateway/` |
| `REF-CTX-0001` | Portable Context Loader + Checkpoint Validator v0.1 | IMPLEMENTED / UNEXECUTED | `context_loader/` |

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
- standard-library unit tests.

The loader returns a retrieval plan only. Bundle matches and retrieved repository records do not create truth or authority.

## Status vocabulary

- `SPECIFIED` — implementation design exists but code does not.
- `IMPLEMENTED / UNEXECUTED` — code exists but repository-preserved test results do not yet exist.
- `TESTED` — tests were executed and exact results were preserved.
- `REPLICATED` — an independent environment reproduced the tested result.
- `FAILED` — implementation did not meet preregistered criteria.
- `DEPRECATED` — retained for history, no longer the active reference.

## Rule

Code existence is not evidence of conformance.

A reference implementation may move to `TESTED` only when the exact revision, interpreter/runtime, command, output, and failures are preserved under `experiments/results/` or another explicitly indexed results path.

## Security boundary

Reference implementations must default to inert simulated resources or metadata planning. Adding real external capabilities requires a separate security review and explicit authorization; research convenience is not sufficient justification.
