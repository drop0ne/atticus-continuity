# Externalized Agent Memory

**Status:** SUPPORTED CONCEPT / RESEARCH TARGET

## Definition

Externalized agent memory is persistent state stored outside an individual model context that later agent runs can discover, inherit, modify, or extend.

Conceptually:

```text
A1 discovers x
A1 -> M(x)
A2 reads M(x) and derives x'
A2 -> M(x, x')
A3 begins from accumulated state rather than zero
```

The individual agents may be temporary while the larger system preserves knowledge.

## Why it matters

This changes the unit of analysis from a single model invocation to a composed system:

```text
weights
+ context
+ tools
+ shared environment
+ persistent artifacts
+ repeated runs
+ orchestration
= effective cognitive system
```

Population-level capability may therefore improve even when no individual model weights change.

## Benefits

Externalized memory can enable:

- division of labor;
- preservation of discoveries;
- reduction of duplicated work;
- cumulative research;
- specialist handoff;
- reproducibility and audit history.

These are desirable properties when authority and objectives are well governed.

## Risks

The same mechanism can preserve:

- unsafe strategies;
- exploits;
- mistaken assumptions;
- deceptive conventions;
- unauthorized capability-expansion techniques;
- contaminated or adversarial instructions.

Persistence therefore amplifies both knowledge and error.

## PAC-compatible treatment

External memory should be epistemically permeable but authority-impermeable:

> **Knowledge can enter. Authority cannot.**

Imported artifacts should not automatically:

- execute;
- invoke tools;
- alter permissions;
- modify canonical policy;
- grant trust to their origin;
- become instructions merely because another agent authored them.

## ATTICUS Continuity relevance

This repository intentionally implements a human-governed form of externalized memory. Its purpose is to preserve useful state across model generations and platform limits while retaining provenance, review, and explicit canonicalization.

The repository itself must therefore be treated as a governed memory substrate, not an autonomous authority source.
