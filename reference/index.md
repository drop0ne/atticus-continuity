# Reference Implementations

Reference code in this directory exists to turn ATTICUS/PAC hypotheses into falsifiable, reproducible experiments.

## Current implementations

| ID | Component | Status | Path |
|---|---|---|---|
| `REF-PAC-GW-0001` | PAC Authority Gateway v0.1 | IMPLEMENTED / UNEXECUTED | `pac_gateway/` |

## Status vocabulary

- `SPECIFIED` — implementation design exists but code does not.
- `IMPLEMENTED / UNEXECUTED` — code exists but repository-preserved test results do not yet exist.
- `TESTED` — tests were executed and exact results were preserved.
- `REPLICATED` — an independent environment reproduced the tested result.
- `FAILED` — implementation did not meet preregistered criteria.
- `DEPRECATED` — retained for history, no longer the active reference.

## Rule

Code existence is not evidence of conformance.

A reference implementation may move to `TESTED` only when the exact revision, interpreter/runtime, command, output, and failures are preserved under `experiments/results/`.

## Security boundary

Reference implementations must default to inert simulated resources. Adding real external capabilities requires a separate security review and explicit authorization; research convenience is not sufficient justification.
