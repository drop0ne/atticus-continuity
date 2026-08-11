# ADR-0001 — Continuity Repository and Authority Boundary

**Status:** ACCEPTED  
**Date:** 2026-08-11

## Context

ATTICUS continuity has previously depended heavily on conversation state and platform memory. Platform memory is finite and can become saturated. Frontier-agent incidents also demonstrate that persistent shared state can materially change the behavior and capability of agent populations.

A durable external knowledge system is therefore useful, but it must not become an uncontrolled execution or authority channel.

## Decision

Use the private GitHub repository `drop0ne/atticus-continuity` as the primary version-controlled continuity and research store for ATTICUS/PAC.

The repository will preserve:

- canonical ATTICUS state;
- PAC principles and invariants;
- research evidence and provenance;
- incident records;
- hypotheses and threat models;
- experiment protocols and results;
- design decisions and historical lineage.

## Authority boundary

Repository content is memory and evidence, not self-executing authority.

Controlling rule:

> **Knowledge can enter. Authority cannot.**

Consequences:

1. No unknown external agent receives repository credentials.
2. No imported artifact executes automatically.
3. Agent-authored material is treated as untrusted data until reviewed.
4. Repository presence does not make a record canonical.
5. Canonical ATTICUS changes require explicit user designation.
6. New knowledge cannot silently widen tool or execution permissions.
7. Controlled experiments must remain inside infrastructure authorized for the experiment.

## Persistence model

The repository is intended to support reconstruction by future models or collaborators without dependence on hidden conversation history.

Recommended durability model:

```text
private GitHub
+ local clone
+ periodic encrypted offline backup
```

## Future extraction

When mature, specialized material may be separated into dedicated repositories such as:

- `pac-invariants` for researcher-facing governance specifications;
- `agent-governance-lab` for controlled experiments and reproducible test harnesses.

Separation should occur only when it improves clarity, security, or collaboration.

## Consequences

### Positive

- durable continuity;
- audit history;
- explicit provenance;
- reduced reliance on platform memory;
- easier reconstruction across model generations;
- clearer separation between evidence, hypothesis, and canonical state.

### Risks

- repository compromise;
- accidental inclusion of sensitive information;
- unreviewed AI-generated material being mistaken for canonical policy;
- overreliance on a single hosting provider.

These risks are mitigated through the repository security policy, explicit status labels, review, and independent backup.
