# Gateway Decision Schema

**Status:** WORKING IMPLEMENTATION SPECIFICATION

A gateway decision is the auditable result of evaluating a proposed consequential action against authority, target, capability, resource, trusted action correlation, uncertainty, and system-state constraints.

```yaml
id: GWD-YYYY-NNNN
timestamp:
proposal_ref:
subject:
authority_ref:
target_scope_ref:
intent_ref:
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
  trusted_correlation: PASS
  route_substitution: PASS
  real_world_effect: PASS
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

## Decision precedence

`ALLOW` requires every mandatory check to pass.

A hard `FAIL` dominates an escalation request. If there is no hard failure but one or more mandatory checks require human/policy resolution, the result may be `ESCALATE`.

```text
hard FAIL -> DENY
else ESCALATE requested -> ESCALATE
else all mandatory PASS -> ALLOW
else -> DENY
```

A failed mandatory check cannot be overridden by model confidence, peer consensus, reward pressure, urgency, task difficulty, or route substitution.

## Trusted correlation

`intent_ref` is supplied by a trusted correlation layer described by `schemas/action-intent-binding.md`. An agent's own `semantic_action_id` is descriptive input, not the security identity used to determine whether a new route is equivalent to a previously denied intent.

Missing trusted correlation prevents `ALLOW`; the reference implementation escalates an otherwise valid proposal so a trusted layer can bind it before execution.

## Reason-code examples

- `NO_AUTHORITY_PROVENANCE`
- `TARGET_NOT_AUTHORIZED`
- `TARGET_AMBIGUOUS`
- `CAPABILITY_OUT_OF_SCOPE`
- `RESOURCE_OUT_OF_SCOPE`
- `AUTHORITY_EXPIRED`
- `AUTHORITY_REVOKED`
- `UNTRUSTED_ARTIFACT_DEPENDENCY`
- `CIRCUIT_BREAKER_OPEN`
- `UNCERTAINTY_REQUIRES_ESCALATION`
- `NO_TRUSTED_ACTION_CORRELATION`
- `ACTION_CORRELATION_AUTHORITY_MISMATCH`
- `SUBSTITUTION_AFTER_DENIAL`
- `REAL_WORLD_EFFECT_NOT_AUTHORIZED`

## Audit requirement

Every consequential decision should produce an immutable or tamper-evident audit event sufficient to reconstruct what was proposed, what authority was presented, which trusted intent was bound, which checks ran, and why the decision was made.
