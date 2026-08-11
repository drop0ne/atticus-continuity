# ADR-0005 — Reference Implementations Are Inert by Default

**Status:** ACCEPTED AS RESEARCH IMPLEMENTATION POLICY  
**Date:** 2026-08-11

## Context

ATTICUS/PAC now has enough structured governance material to support executable reference implementations. Executable code creates a new risk: a research harness could accidentally become a bridge from conceptual safety work into uncontrolled interaction with real systems.

## Decision

Reference implementations in `atticus-continuity` are inert by default.

They may implement:

- deterministic policy evaluation;
- synthetic agents;
- simulated resources;
- local state machines;
- test fixtures;
- audit generation;
- conformance measurement.

They must not acquire real-world execution capability merely because such capability would make a demonstration more realistic.

## Explicitly excluded by default

- network probing;
- autonomous discovery of external agents;
- shell/subprocess execution against external systems;
- third-party credentials;
- live exploit execution;
- automatic interaction with public accounts or repositories;
- real-world target manipulation.

Any future exception requires a separate authorization and security decision record.

## Evidence rule

Implementation status and experimental evidence are separate states.

```text
specified != implemented != tested != replicated
```

The repository must not label tests as passing until they have actually been executed and the exact revision, runtime, command, and results are preserved.

## Consequence

The first PAC Authority Gateway implementation is suitable for controlled local conformance work but is not a production security system and is not authorized as an interface to external autonomous systems.
