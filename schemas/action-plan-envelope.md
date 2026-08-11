# Action Plan Envelope Schema

**Status:** WORKING IMPLEMENTATION SPECIFICATION

An action-plan envelope binds multiple substeps to a trusted aggregate purpose so governance can evaluate both local actions and cumulative effects without treating plan membership as local authority.

```yaml
id: PLAN-YYYY-NNNN
issuer:
created_at:
expires_at:
objective:
subjects: []
authorized_authority_refs:
  <subject>:
    - AUTH-YYYY-NNNN
target_scope_refs: []
allowed_capabilities: []
allowed_resources: []
allowed_effects: []
forbidden_aggregate_effects: []
step_limit:
resource_budgets:
  <resource>: <max_units>
effect_budgets:
  <effect>: <max_units>
correlation_basis:
status: ACTIVE
provenance:
```

## Rules

1. The plan envelope is assigned or verified by a trusted orchestration layer, not created as authority by the agents performing the work.
2. Every consequential substep associated with the plan must independently pass the normal PAC Authority Gateway.
3. Plan membership does not confer local authority. Each subject must present a valid authority reference explicitly bound to that subject in `authorized_authority_refs`.
4. Different subjects may use different independently bounded authority chains under one aggregate plan.
5. Aggregate plan state must remain within explicit plan budgets and effect scope.
6. Missing plan scope does not mean unlimited scope.
7. Changing agents, authority tokens, tools, or routes does not reset aggregate counters.
8. Creating a new plan ID does not itself create new authority.
9. Aggregate budget evaluation and reservation should be atomic relative to the plan state.

## Decision relation

A substep may execute only when:

```text
local_gateway(step) == ALLOW
AND
subject_authority_is_bound(plan, step) == true
AND
aggregate_plan_check(plan, step) == ALLOW
```

## Cross-agent property

For agents `A` and `B` operating under distinct valid authority grants:

```text
usage(plan, A) + usage(plan, B) <= aggregate_budget(plan)
```

Changing the acting agent or authority token does not create a fresh aggregate budget.

## Purpose

This object addresses group-level authority laundering in which individually benign-looking actions compose into an unauthorized aggregate outcome, while preserving the requirement that every participating agent possess its own valid local authority.
