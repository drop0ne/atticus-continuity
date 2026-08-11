# Authority Token Schema

**Status:** WORKING IMPLEMENTATION SPECIFICATION

An authority token is a non-secret logical object representing bounded permission. It is not itself a credential to a third-party system.

```yaml
id: AUTH-YYYY-NNNN
issuer:
subject:
issued_at:
expires_at:
objective_scope: []
target_scope_refs: []
capability_scope: []
resource_scope: []
constraints: []
delegation_allowed: false
max_delegation_depth: 0
parent_authority_ref:
revocation_ref:
provenance:
  decision_record:
  human_or_service:
status: ACTIVE
```

## Required properties

- Explicit issuer and subject.
- Explicit capability and target scope.
- Finite lifetime where practical.
- Provenance to an authorized decision or policy.
- No implicit wildcard expansion from missing fields.
- Missing scope is interpreted as **not authorized**, not "all".

## Validation rule

A proposed action is authorized only if every consequential dimension is a subset of the token:

```text
objective(action)  subset_of objective_scope(token)
target(action)     subset_of target_scope(token)
capability(action) subset_of capability_scope(token)
resource(action)   subset_of resource_scope(token)
time(action)       within token lifetime
```

Failure of any check yields deny or authorized escalation.

## Non-properties

An authority token does not establish that:

- an action is wise;
- a factual premise is true;
- a target is actually relevant;
- a model is aligned;
- execution is technically safe.

Those require separate checks.
