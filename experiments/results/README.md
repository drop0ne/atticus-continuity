# Experiment Results

This directory stores **executed evidence**, not proposed tests.

## Admission rule

A file belongs here only after a test or experiment actually ran.

For each run preserve, where practical:

- experiment ID;
- implementation ID;
- exact repository revision;
- runtime/interpreter version;
- operating platform;
- command used;
- tests/scenarios actually executed;
- failures, errors, skips, and anomalies;
- whether preregistered pass criteria were met;
- reviewer and review date when applicable.

Use `schemas/experiment-result.md` as the baseline record structure.

## Evidence integrity

Never replace an earlier failed result with a later successful result. New runs receive new result IDs and remain linked to their exact software revision.

A later code revision does not inherit an earlier revision's passing status merely because the same tests are expected to pass.

## Recorded results

| Result | Experiment | Revision | Outcome |
|---|---|---|---|
| `RES-2026-0001-exp0004-f3ed8958.json` | `EXP-0004` / `REF-PAC-GW-0001` | `f3ed8958b3b819852d4a634f718a097f95b65114` | PASS — 36/36, 0 failures, 0 errors, 0 skipped |
| `RES-2026-0002-exp0005-81f95736.json` | `EXP-0005` / `REF-PAC-GW-0001` | `81f95736f8e0adbe1ef13bf66bbee26d1ba11099` | PASS — 10/10, 0 failures, 0 errors, 0 skipped |
| `RES-2026-0003-exp0006-81f95736.json` | `EXP-0006` / `REF-PAC-GW-0001` | `81f95736f8e0adbe1ef13bf66bbee26d1ba11099` | PASS — 10/10, 0 failures, 0 errors, 0 skipped |

The first recorded EXP-0004 execution ran in a repository-controlled GitHub Actions job on CPython 3.12.3 / Ubuntu 24.04. The result is evidence for that exact inert reference revision only; it is not proof of production security, general alignment, distributed correctness, or arbitrary semantic-equivalence detection.

EXP-0005 and EXP-0006 were executed in GitHub Actions run `31983045378`, job `95253129558`, against exact revision `81f95736f8e0adbe1ef13bf66bbee26d1ba11099` with repository token permissions limited to `contents: read` and `metadata: read`. EXP-0005 covers aggregate plan-budget persistence, subject-bound plan authority, unknown-plan rejection, snapshot integrity, and a two-thread final-budget race. EXP-0006 adds dedicated scenario coverage for trusted correlation, relabel evasion, invalid bindings, new grants, and escalation resolution. These results remain exact-revision evidence only.
