# PAC Authority Gateway — Reference Implementation v0.1

**Status:** RESEARCH PROTOTYPE / NOT PRODUCTION SECURITY  
**Scope:** deterministic, inert, local sandbox logic only.

This directory turns the PAC Authority Gateway working architecture into executable reference code for controlled conformance testing.

## Security boundary

The implementation intentionally provides **no**:

- network access;
- shell or subprocess execution;
- filesystem mutation API;
- browser control;
- package-manager access;
- third-party credentials;
- autonomous agent discovery or communication.

The `ConstrainedExecutor` records a synthetic effect only after an `ALLOW` decision.

## Core property under test

```text
execute(action) -> valid_authority(action)
```

The implementation does not accept `model believes this is authorized` as an authority source.

## Implemented checks

- explicit authority provenance;
- token status and lifetime;
- objective scope;
- target-scope reference and identifier matching;
- capability scope;
- resource scope;
- target-effect scope;
- explicit real-world-effect permission;
- delegated-token subset monotonicity;
- delegation-record subset validation;
- uncertainty fail-closed/escalation behavior;
- persistent artifact authority rejection;
- peer consensus non-authority;
- sticky route-denial correlation under the same authority grant;
- circuit-breaker restriction/open behavior;
- tamper-evident SHA-256 audit chaining;
- constrained executor refusal when the gateway does not return `ALLOW`.

## Run tests

From the repository root with Python 3.11+:

```bash
python -m unittest reference.pac_gateway.test_gateway -v
```

No third-party Python packages are required.

## Important trust assumptions

### `semantic_action_id`

Route-substitution detection currently depends on `semantic_action_id`. For security-relevant use, this value **must be assigned or verified by a trusted orchestration/correlation layer**, not accepted blindly from the agent being governed. If an untrusted agent can choose arbitrary semantic IDs, it may evade simple substitution correlation by renaming the same intended action.

This is a known v0.1 limitation and should be treated as a research target, not a solved control.

### Authority-token integrity

The reference objects are in-memory Python data structures. They are not cryptographically signed tokens. A production design would need authenticated policy state, protected issuance/revocation, replay controls, durable storage, and concurrency-safe validation.

### Target identity

The implementation uses exact identifier-set matching. It does not solve real-world identity verification. Identity binding should be performed by an independently trusted resolver before consequential execution.

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
- semantic equivalence detection across arbitrary novel routes;
- safety of connecting the prototype to real systems.

The reference implementation exists to make PAC invariants falsifiable and testable, not to claim that they have already been solved.
