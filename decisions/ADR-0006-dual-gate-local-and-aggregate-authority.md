# ADR-0006 — Consequential Multi-Step Work Requires Local and Aggregate Authority

**Status:** ACCEPTED AS RESEARCH ARCHITECTURE  
**Date:** 2026-08-11

## Context

The PAC Authority Gateway evaluates individual proposed actions. In multi-step and multi-agent systems, individually permitted actions can compose into an aggregate outcome outside the original authority grant.

## Decision

For correlated consequential work, require two independent authorization conditions:

```text
local_gateway(step) == ALLOW
AND
aggregate_plan_gate(plan, step) == ALLOW
```

Neither gate repairs failure of the other.

## Consequences

- Plans carry trusted authority and correlation references.
- Aggregate budgets survive changes in tool, route, and step identity.
- Unknown or agent-invented plan IDs do not grant authority.
- Local agent authority remains mandatory even when the agent belongs to an authorized plan.
- Aggregate budget updates should be atomic.
- Plan membership or coordination does not create new authority.

## Research limitation

The initial reference implementation can enforce explicitly represented step/resource/effect budgets. It cannot prove that arbitrary sequences are semantically equivalent to a prohibited aggregate action.

That limitation is preserved as an open research target rather than hidden behind the term `aggregate authority`.
