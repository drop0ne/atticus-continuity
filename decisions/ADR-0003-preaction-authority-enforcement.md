# ADR-0003 — Pre-Action Authority Enforcement

**Status:** ACCEPTED AS RESEARCH ARCHITECTURE  
**Date:** 2026-08-11

## Context

Current incident-derived threat models indicate that instruction-level scope recognition, post-action monitoring, and endpoint-specific blocking may be insufficient for highly capable, tool-using, multi-agent systems.

The recurring governance problem is that a model may discover a useful action path that was not explicitly authorized, while human review may occur too late to prevent execution.

## Decision

For high-consequence agent research, ATTICUS/PAC will treat **pre-action external authority enforcement** as the default architecture hypothesis.

Conceptually:

```text
agent proposal
-> authority provenance check
-> objective/target/capability validation
-> capability gateway
-> execution or fail-closed denial
```

The model may reason about whether an action should be allowed, but its own conclusion is not the final authority source.

## Human role

Human review should be concentrated at meaningful authority transitions, including:

- expansion of target scope;
- introduction of a new capability class;
- delegation of authority;
- exception or emergency authority;
- promotion of untrusted artifacts into trusted reusable state.

Human review is not assumed to scale to every low-level machine-speed action.

## Consequences

### Benefits

- separates cognition from permission;
- provides an auditable authority chain;
- can prevent action before monitoring latency becomes relevant;
- supports group-level and multi-agent governance;
- creates a concrete surface for adversarial testing.

### Costs and risks

- false denials may impair legitimate capability;
- authority services may become bottlenecks or single points of failure;
- novel actions may be difficult to classify;
- poorly designed gates can create incentives for substitution attempts;
- the authority service itself requires strong security and governance.

## Validation requirement

This decision records the architecture to be tested, not a claim that it is already effective. `EXP-0001` and `EXP-0003` are intended to measure whether it materially improves outcomes.
