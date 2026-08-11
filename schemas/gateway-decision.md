# Gateway Decision Schema

**Status:** WORKING IMPLEMENTATION SPECIFICATION

A gateway decision is the auditable result of evaluating a proposed consequential action against authority, target, capability, resource, uncertainty, and system-state constraints.

```yaml
id: GWD-YYYY-NNNN
timestamp:
proposal_ref:
subject:
authority_ref:
target_scope_ref:
checks:
  authority_provenance: PASS
  objective_scope: PASS
  target_scope: PASS
  capability_scope: PASS
  resource_scope: PASS
  time_scope: PASS
  delegation_chain: PASS
  artifact_trust: PASS
  circuit_breaker: PASS
  uncertainty_policy: PASS
decision: DENY
reason_codes: []
escalation_path:
audit_event_ref:
```

## Allowed decisions

- `ALLOW`
- `DENY`
- `ESCALATE`
- `DEFER`

## Decision rule

`ALLOW` requires every mandatory check to pass.

A failed mandatory check cannot be overridden by model confidence, peer consensus, reward pressure, urgency, task difficulty, or route substitution.

## Reason-code examples

- `NO_AUTHORITY_PROVENANCE`
- `TARGET_NOT_AUTHORIZED`
- `TARGET_AMBIGUOUS`
- `CAPABILITY_OUT_OF_SCOPE`
- `RESOURCE_OUT_OF_SCOPE`
- `DELEGATION_EXCEEDS_PARENT`
- `AUTHORITY_EXPIRED`
- `AUTHORITY_REVOKED`
- `UNTRUSTED_ARTIFACT_DEPENDENCY`
- `CIRCUIT_BREAKER_OPEN`
- `UNCERTAINTY_REQUIRES_ESCALATION`
- `SUBSTITUTION_AFTER_DENIAL`

## Audit requirement

Every consequential decision should produce an immutable or tamper-evident audit event sufficient to reconstruct what was proposed, what authority was presented, which checks ran, and why the decision was made.
