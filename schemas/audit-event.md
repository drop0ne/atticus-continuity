# Audit Event Schema

**Status:** WORKING IMPLEMENTATION SPECIFICATION

Audit events preserve sufficient evidence to reconstruct consequential decisions without depending on model memory or narrative summaries.

```yaml
id: EVT-YYYY-NNNN
timestamp:
event_type:
actor:
agent_run_id:
objective_ref:
proposal_ref:
authority_ref:
intent_ref:
target_scope_ref:
gateway_decision_ref:
circuit_breaker_ref:
artifact_refs: []
parent_event_refs: []
checks: {}
result:
reason_codes: []
model_statement:
external_observation:
integrity:
  previous_event_hash:
  event_hash:
```

## Event types

Examples:

- `ACTION_PROPOSED`
- `ACTION_ALLOWED`
- `ACTION_DENIED`
- `ACTION_ESCALATED`
- `ACTION_CORRELATED`
- `DELEGATION_CREATED`
- `DELEGATION_REJECTED`
- `TARGET_AMBIGUITY_DETECTED`
- `SUBSTITUTION_ATTEMPT`
- `ARTIFACT_IMPORTED`
- `ARTIFACT_PROMOTED`
- `CIRCUIT_BREAKER_OPENED`
- `CIRCUIT_BREAKER_RELEASED`

## Separation rule

Where possible, record separately:

- what the model said it intended;
- what action it proposed;
- the trusted `intent_ref` assigned by the correlation layer;
- what authority it presented;
- what the gateway decided;
- what actually happened in the environment.

Do not equate chain-of-thought-style statements, an agent's own action label, or an externally assigned correlation key with ground-truth causality. Each is a different evidence type.

## Integrity objective

Logs should be append-only or tamper-evident in implementations intended for meaningful evaluation. An agent being evaluated should not be able to rewrite the evidence used to evaluate it.

The local reference implementation chains event hashes from `GENESIS`. This detects mutation within the retained sequence but is not equivalent to an externally anchored append-only audit service.
