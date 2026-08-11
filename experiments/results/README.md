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

## Current state

No EXP-0004 passing result is recorded merely because the reference implementation and test suite exist. Until execution output is captured, its status remains `IMPLEMENTED / UNEXECUTED`.
