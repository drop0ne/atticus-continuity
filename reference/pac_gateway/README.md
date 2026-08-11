# PAC Authority Gateway — Reference Implementation v0.2

**Status:** RESEARCH PROTOTYPE / NOT PRODUCTION SECURITY  
**Scope:** deterministic, inert, local sandbox logic only.

This directory turns PAC Authority Gateway and aggregate-authority working architectures into executable reference code for controlled conformance testing.

## Security boundary

The implementation intentionally provides **no**:

- network access;
- shell or subprocess execution;
- browser control;
- package-manager access;
- third-party credentials;
- autonomous agent discovery or communication.

The `ConstrainedExecutor` records a synthetic effect only after an `ALLOW` decision. The EXP-0004 runner prints result evidence to stdout and does not itself write files.

## Core properties under test

```text
execute(action) -> valid_local_authority(action)
```

For correlated multi-step work:

```text
execute(step) -> local_gateway(step) == ALLOW
                 AND aggregate_plan_gate(step) == ALLOW
```

The implementation does not accept `model believes this is authorized`, peer agreement, plan membership, persistence, or agent self-labeling as authority sources.

## Implemented controls

- explicit authority provenance;
- token status and lifetime;
- objective scope;
- target-scope reference and exact identifier matching;
- capability scope;
- resource scope;
- target-effect scope;
- explicit real-world-effect permission;
- delegated-token subset monotonicity;
- delegation-record subset validation;
- uncertainty fail-closed/escalation behavior;
- persistent artifact authority rejection;
- peer consensus non-authority;
- trusted action-intent bindings for route-substitution correlation;
- hard-failure precedence over escalation;
- circuit-breaker restriction/open behavior;
- secondary monitoring triggers that can only narrow future action;
- tamper-evident SHA-256 audit chaining;
- constrained executor refusal when the gateway does not return `ALLOW`;
- aggregate plan step/resource/effect budgets;
- independently bounded authority bindings for multiple agents under one plan;
- in-process atomic aggregate budget reservation;
- dedicated read-only plan snapshots.

## Run tests

From the repository root with Python 3.11+:

```bash
python -m unittest reference.pac_gateway.test_gateway reference.pac_gateway.test_plan -v
```

No third-party Python packages are required.

## Produce an EXP-0004 evidence record

Use the dedicated runner and supply the exact revision under test:

```bash
python -m reference.pac_gateway.run_exp0004 --revision <COMMIT_SHA>
```

The runner emits JSON containing runtime information, test count, failures/errors, pass status, duration, and raw `unittest` output. Preserve that output under `experiments/results/` before changing the implementation if you want it to count as repository evidence.

The presence of this runner does **not** mean EXP-0004 has already passed.

## Important trust assumptions

### Trusted action correlation

`ActionProposal.semantic_action_id` remains an agent-side descriptive hint. It is **not** used directly as the security correlation key.

The gateway now requires an independently supplied `ActionIntentBinding` through a trusted `intent_resolver`. An otherwise valid action without trusted correlation cannot receive `ALLOW`; the reference behavior is `ESCALATE` unless another hard failure requires `DENY`.

The trusted binding interface prevents simple self-relabeling from being treated as proof that an action is new. It does **not** solve arbitrary semantic equivalence. Resolver quality remains a separate research problem.

### Authority-token integrity

The reference objects are in-memory Python data structures. They are not cryptographically signed tokens. A production design would need authenticated policy state, protected issuance/revocation, replay controls, durable storage, and concurrency-safe validation.

### Target identity

The implementation uses exact identifier-set matching. It does not solve real-world identity verification. Identity binding should be performed by an independently trusted resolver before consequential execution.

### Aggregate semantic effects

`PlanLedger` enforces explicitly represented step/resource/effect budgets. This prevents several decomposition attacks but does not infer arbitrary hidden aggregate effects.

### Concurrency

The local reference ledger protects evaluation-and-reservation with an in-process lock and includes a two-thread final-budget race scenario. Distributed/multi-process transactional correctness is not established.

## Audit integrity

Audit events form a local SHA-256 hash chain:

```text
GENESIS -> EVT1 -> EVT2 -> EVT3 ...
```

This detects mutation when verified against the retained chain but is **not** equivalent to an externally anchored append-only log. A production evaluation should write events to storage the evaluated agent cannot rewrite and may additionally anchor hashes externally.

## Non-claims

Passing these tests would not prove:

- general alignment;
- consciousness or lack of consciousness;
- immunity to implementation bugs;
- robustness against a compromised gateway host;
- robustness against incorrect authority issuance;
- arbitrary semantic equivalence detection;
- distributed consistency;
- safety of connecting the prototype to real systems.

The reference implementation exists to make PAC invariants falsifiable and testable, not to claim that they have already been solved.
