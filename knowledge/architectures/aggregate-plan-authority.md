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
      |
      +-- DENY / ESCALATE --> stop
      |
      v
AGGREGATE PLAN LEDGER
  |-- trusted plan identity
  |-- plan authority binding
  |-- subject membership
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

Likewise, semantic-action correlation used for route-substitution detection should not depend solely on untrusted self-labeling by the agent.

## Budgets

The reference architecture currently represents:

- maximum step count;
- resource-unit budgets;
- effect-unit budgets.

These are deliberately explicit and mechanically checkable.

They do not solve arbitrary semantic composition. A sequence may create a harmful aggregate outcome not represented by any configured budget. That remains an open research problem.

## Concurrency

Budget evaluation and commit must be atomic with respect to the relevant plan state. Otherwise parallel agents can each observe remaining capacity and collectively oversubscribe it.

The v0.1 local reference implementation uses an in-process lock. Distributed deployments would require a transactional or otherwise concurrency-safe authority store.

## Cross-agent authority

A shared plan may legitimately contain multiple agents, but each agent still requires its own valid local authority chain. Plan membership is not a substitute for agent-level authorization.

A future reference revision should represent multiple independently bounded authority chains under one aggregate plan and demonstrate that changing agents does not reset plan budgets.

## Security relation

This architecture extends rather than replaces the PAC Authority Gateway:

```text
local authority
+ aggregate authority
+ circuit breaker
+ audit integrity
```

Each addresses a different failure surface.
