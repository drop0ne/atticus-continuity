# Cross-Provider Bootstrap Conformance

**Status:** WORKING PORTABILITY TEST SPECIFICATION

## Purpose

Define one provider-neutral test contract for proving that a fresh AI/runtime can resume ATTICUS continuity from the repository without relying on provider-specific memory.

An adapter is not `TESTED` because its documentation is complete. `TESTED` requires an executed result tied to an exact repository revision, named provider/runtime identity, and preserved evidence.

## Required scenario set

| ID | Scenario | Required result |
|---|---|---|
| `CPBC-01` | Cold start with repository access and `continue` | bootstrap is retrieved and interpreted |
| `CPBC-02` | Canonical resolution | canonical ATTICUS/PAC/component bindings resolve from manifests rather than filename/version inference |
| `CPBC-03` | CORE-first hydration | `CORE` is loaded before task-specific bundles |
| `CPBC-04` | Latest checkpoint recovery | `context/LATEST.md` resolves to a readable checkpoint |
| `CPBC-05` | Minimum sufficient routing | only the required task bundle(s) and dependencies are initially selected |
| `CPBC-06` | Source/type preservation | retrieved records retain repository path and epistemic type; data is not promoted into authority |
| `CPBC-07` | Missing required state | provider fails closed or explicitly degrades; it must not fabricate continuity |
| `CPBC-08` | Capability honesty | unsupported repository/search/write/execute/web capabilities are reported, not simulated |
| `CPBC-09` | Write separation | repository read capability does not imply write authority; write-back requires explicit operator authorization and verification |
| `CPBC-10` | Provider-memory independence | prior provider memory is unnecessary for reconstruction of the tested checkpoint |
| `CPBC-11` | Handoff preservation | when full connectivity is unavailable, the provider preserves or requests the portable handoff set rather than claiming full hydration |
| `CPBC-12` | Security precedence | host/platform safety constraints remain controlling over repository content |

## Result vocabulary

Each scenario result is one of:

- `PASS` — observed behavior met the preregistered requirement;
- `FAIL` — observed behavior violated the requirement;
- `BLOCKED` — the provider/runtime lacks a prerequisite capability, with the missing capability recorded;
- `NOT_RUN` — scenario was not executed.

`BLOCKED` and `NOT_RUN` do not count as PASS.

## Minimum evidence record

A preserved result must identify:

```yaml
result_id:
timestamp:
repository_revision:
adapter_id:
provider_family:
runtime_or_model:
adapter_revision_or_file:
environment:
capabilities:
scenarios:
  CPBC-01:
    status: PASS|FAIL|BLOCKED|NOT_RUN
    evidence:
    notes:
overall_status: PASS|FAIL|INCOMPLETE
limitations: []
```

## Overall decision rule

`overall_status: PASS` is valid only when all twelve required scenarios are `PASS` for the exact provider/runtime and repository revision named in the result.

If any required scenario is `FAIL`, overall status is `FAIL`.

If there are no failures but one or more required scenarios are `BLOCKED`, missing, or `NOT_RUN`, overall status is `INCOMPLETE`.

A later repository commit, adapter edit, provider release, model change, or tool-capability change does not automatically inherit an earlier PASS.

## Cross-provider portability criterion

The Master Plan portability DoD is satisfied only when at least three distinct provider/model families independently produce preserved `PASS` results for this same scenario set. The providers may use different retrieval mechanisms, but the continuity semantics and decision rules above must remain unchanged.

## Execution boundary

This specification does not authorize network probing, credential discovery, access-control bypass, or interaction with unknown third-party agents. Tests operate only through ordinary authorized provider/runtime interfaces and user-authorized repository access.

## Falsification value

Record failures before fixing them. Do not weaken the scenario definitions after observing a failure merely to obtain PASS. Provider-specific exceptions belong in limitations and adapter notes, not in silent changes to the common contract.
