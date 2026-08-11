# ADR-0004 — Represent Authority as Structured Data

**Status:** ACCEPTED AS RESEARCH ARCHITECTURE  
**Date:** 2026-08-11

## Context

Instruction-only scope can be interpreted by the same model that is optimizing for task completion. Frontier-agent incidents motivate testing architectures where authority is represented outside model cognition and checked before consequential action.

## Decision

Represent operational authority as structured, machine-checkable state rather than relying only on natural-language instructions.

Core objects:

- authority token;
- target-scope object;
- delegation record;
- artifact trust label;
- gateway decision;
- circuit-breaker state;
- audit event.

## Decision semantics

A model may propose an action but does not determine whether the proposal is authorized.

The external gateway evaluates whether the proposal is a subset of valid authority state.

```text
proposal
-> structured authority checks
-> ALLOW / DENY / ESCALATE / DEFER
```

## Consequences

### Advantages

- explicit provenance;
- auditable delegation;
- deterministic subset checks where possible;
- separation between belief and permission;
- clearer falsification tests;
- machine-speed enforcement compatible with machine-speed agents.

### Costs and risks

- schema complexity;
- policy-authoring mistakes;
- false denials from overly narrow scope;
- false allows from bad target identity or policy encoding;
- gateway implementation becoming a critical security boundary;
- pressure to create dangerous wildcard exceptions for convenience.

## Constraints

- Missing fields narrow authority.
- No wildcard default from omission.
- Delegation cannot exceed parent authority.
- Uncertainty cannot increase authority.
- Gateway failure must fail closed for consequential actions.
- Human override, where allowed, must create a new bounded authority record rather than silently bypass the gateway.

## Status caveat

This decision adopts the architecture for experimentation. It does not establish that the architecture is sufficient for frontier-model safety.
