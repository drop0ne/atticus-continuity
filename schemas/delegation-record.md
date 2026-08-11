# Delegation Record Schema

**Status:** WORKING IMPLEMENTATION SPECIFICATION

A delegation record represents bounded transfer of existing authority from one subject to another.

```yaml
id: DEL-YYYY-NNNN
parent_authority_ref:
delegator:
delegatee:
issued_at:
expires_at:
objective_scope: []
target_scope_refs: []
capability_scope: []
resource_scope: []
constraints: []
further_delegation_allowed: false
remaining_delegation_depth: 0
status: ACTIVE
```

## Monotonicity rule

Delegation may preserve or reduce authority. It may never increase it.

```text
Authority(delegatee) subset_of Authority(delegator)
```

Each field in a child delegation must be a subset of the corresponding parent field.

## Invalid delegation

Reject if:

- parent authority cannot be resolved;
- parent authority is expired or revoked;
- requested scope exceeds parent scope;
- delegation is forbidden by the parent;
- remaining delegation depth would become negative;
- target identity is ambiguous;
- provenance is missing.

Peer agreement cannot repair an invalid delegation.
