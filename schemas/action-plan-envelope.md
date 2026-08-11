# Action Plan Envelope Schema

**Status:** WORKING IMPLEMENTATION SPECIFICATION

An action-plan envelope binds multiple substeps to a trusted aggregate purpose so governance can evaluate both local actions and cumulative effects.

```yaml
id: PLAN-YYYY-NNNN
issuer:
created_at:
expires_at:
authority_ref:
objective:
subjects: []
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
3. Aggregate plan state must remain within explicit plan budgets and effect scope.
4. Missing plan scope does not mean unlimited scope.
5. Changing agents, tools, or routes does not reset aggregate counters.
6. Creating a new plan ID does not itself create new authority.

## Decision relation

A substep may execute only when:

```text
local_gateway(step) == ALLOW
AND
aggregate_plan_check(plan, step) == ALLOW
```

## Purpose

This object addresses group-level authority laundering in which individually benign-looking actions compose into an unauthorized aggregate outcome.
