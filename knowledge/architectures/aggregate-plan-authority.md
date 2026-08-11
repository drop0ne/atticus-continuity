# Aggregate Plan Authority

**Status:** WORKING ARCHITECTURE

## Problem

Per-action authorization is necessary but not sufficient for multi-agent systems.

A sequence can be unsafe even when each local action is individually permitted:

```text
ALLOW(step_1)
ALLOW(step_2)
ALLOW(step_3)
```

does not imply:

```text
ALLOW(step_1 + step_2 + step_3)
```

This is the decomposition/authority-laundering problem captured by PAC-INV-0010.

## Architecture

```text
AGENT / PLANNER
      |
      v
ACTION PROPOSAL
      |
      v
PAC LOCAL AUTHORITY GATEWAY
  |-- local authority chain
  |-- target / capability / resource scope
  |-- trusted action correlation
      |
      +-- DENY / ESCALATE --> stop
      |
      v
AGGREGATE PLAN LEDGER
  |-- trusted plan identity
  |-- subject -> permitted authority references
  |-- target scope
  |-- capability scope
  |-- resource scope
  |-- effect scope
  |-- step budget
  |-- resource budget
  |-- effect budget
      |
      +-- DENY --> stop + audit
      |
      v
CONSTRAINED EXECUTOR
```

## Dual-gate property

For consequential substep `s` under plan `p`:

```text
execute(s) -> local_authority(s) AND aggregate_authority(p, s)
```

Aggregate approval cannot repair a local denial, and local approval cannot bypass aggregate limits.

## Trusted correlation

Plan identity is security-relevant state.

A plan ID should be created, assigned, or verified by a trusted orchestration layer. An evaluated agent must not be able to reset cumulative limits merely by inventing a new identifier.

Route-substitution correlation is separately represented by `ActionIntentBinding`. The agent's own semantic label is descriptive input rather than the security key used to decide whether a route is equivalent to a previously denied intent.

## Budgets

The reference architecture currently represents:

- maximum step count;
- resource-unit budgets;
- effect-unit budgets;
- per-subject committed-step counts for reconstruction.

These are deliberately explicit and mechanically checkable.

They do not solve arbitrary semantic composition. A sequence may create a harmful aggregate outcome not represented by any configured budget. That remains an open research problem.

## Concurrency

Budget evaluation and commit must be atomic with respect to the relevant plan state. Otherwise parallel agents can each observe remaining capacity and collectively oversubscribe it.

The v0.2 local reference implementation uses an in-process lock and includes a two-thread test in which two independently authorized agents race for the final unit of aggregate budget. The intended property is that at most one reservation commits.

Distributed and multi-process deployments would still require a transactional or otherwise concurrency-safe authority store. Local lock behavior is not evidence of distributed correctness.

## Cross-agent authority

A shared plan may legitimately contain multiple agents, but each agent still requires its own valid local authority chain. Plan membership is not a substitute for agent-level authorization.

The current plan envelope binds permitted authority references by subject:

```text
authorized_authority_refs[subject] -> {valid local authority refs}
```

This permits multiple independently bounded agent authorities under one aggregate plan while retaining one shared set of aggregate counters.

Therefore:

```text
change agent != reset plan budget
change local authority token != reset plan budget
```

provided the new token is independently valid and explicitly bound to that subject under the same plan.

## Snapshot semantics

Aggregate state is exposed through a dedicated `PlanSnapshot` rather than by manufacturing a fake gateway/plan decision. This keeps observation of state separate from authorization outcomes.

## Security relation

This architecture extends rather than replaces the PAC Authority Gateway:

```text
local authority
+ trusted action correlation
+ aggregate authority
+ circuit breaker
+ audit integrity
```

Each addresses a different failure surface.
