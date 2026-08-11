# Experiment Result Schema

**Status:** WORKING IMPLEMENTATION SPECIFICATION

Experiment results are evidence records. They must preserve enough information to distinguish an implementation claim from an actually executed test.

```yaml
id: RES-YYYY-NNNN
experiment_ref:
implementation_ref:
status: EXECUTED
executed_at:
operator:
revision:
runtime:
  language:
  version:
  platform:
command:
expected_suite:
observed:
  tests_run:
  passed:
  failures:
  errors:
  skipped:
  duration_seconds:
artifacts:
  stdout_ref:
  stderr_ref:
  audit_refs: []
pass_criteria_met: false
anomalies: []
limitations: []
reviewer:
reviewed_at:
```

## Evidence rule

A result is not valid merely because a test file exists.

At minimum preserve:

- exact repository revision;
- runtime/interpreter version;
- execution command;
- number of tests actually run;
- failures and errors;
- whether preregistered pass criteria were met.

## Status distinctions

- `UNEXECUTED` — no test run evidence exists.
- `EXECUTED` — test command ran and output was captured.
- `PASS` — executed result met the preregistered pass criteria.
- `FAIL` — executed result failed one or more preregistered criteria.
- `REPLICATED_PASS` — an independent environment reproduced the passing result.
- `REPLICATED_FAIL` — an independent environment reproduced a failure.

## Rule against retroactive success

Do not rewrite an earlier failing run into a passing record after fixing the implementation. Preserve both results and link the later result to the code revision that changed.
