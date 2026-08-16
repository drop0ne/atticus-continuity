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

The first recorded EXP-0004 execution ran in a repository-controlled GitHub Actions job on CPython 3.12.3 / Ubuntu 24.04. The result is evidence for that exact inert reference revision only; it is not proof of production security, general alignment, distributed correctness, or arbitrary semantic-equivalence detection.
