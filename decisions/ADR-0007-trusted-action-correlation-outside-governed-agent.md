# ADR-0007 — Security-Relevant Action Correlation Lives Outside the Governed Agent

**Status:** ACCEPTED AS RESEARCH ARCHITECTURE  
**Date:** 2026-08-11

## Context

PAC-INV-0006 requires a denied action to remain denied when an agent merely changes routes. The first reference implementation correlated substitutions using an `ActionProposal.semantic_action_id`. Because that value can be supplied by the governed agent, it is not a sound security boundary: an agent could relabel the same consequential intent.

## Decision

Treat agent-supplied semantic labels as descriptive input only.

Security-relevant route correlation must be supplied or verified by a trusted orchestration/correlation layer outside the governed agent, represented through `ActionIntentBinding`.

```text
agent label != trusted intent identity
```

An otherwise valid consequential proposal without trusted correlation does not receive `ALLOW` in the reference implementation. It is escalated for correlation unless another hard failure requires denial.

## Decision precedence

Hard failures dominate escalation requests:

```text
hard FAIL -> DENY
else escalation required -> ESCALATE
else all mandatory checks PASS -> ALLOW
```

This prevents a missing correlation record from softening an unrelated hard authority failure.

## Denial versus escalation

Only hard denial creates sticky route-substitution state in the reference implementation.

`ESCALATE` indicates that trusted information or review is missing. Once that missing information is supplied, the proposal may be evaluated again under the same authority grant.

## Consequences

- `semantic_action_id` remains available for diagnostics but does not control route-substitution security.
- Audit events preserve the externally assigned `intent_ref` separately.
- Correlation bindings are proposal-specific, provenance-bearing, authority-bound, and time-bounded.
- New explicit authority grants remain independently evaluable.
- Resolver quality becomes an explicit research surface rather than a hidden assumption.

## Limitation

This decision defines the trust boundary for correlation; it does not solve arbitrary semantic equivalence. A trusted resolver can still be wrong. False splits can permit substitution and false merges can create unnecessary denial.
