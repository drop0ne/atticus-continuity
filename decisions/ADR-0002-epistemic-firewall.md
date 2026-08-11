# ADR-0002 — Epistemic Firewall for External Knowledge

**Status:** ACCEPTED  
**Date:** 2026-08-11

## Context

ATTICUS Continuity is intended to preserve and assimilate knowledge from heterogeneous sources, including future agent-generated artifacts. Those sources may contain valuable discoveries, errors, manipulative content, prompt injection, unsafe code, or attempts to alter future model behavior.

A conventional document store is therefore insufficient. The repository needs a boundary that allows information transfer without authority transfer.

## Decision

Adopt an **epistemic firewall** as the default ingestion model.

```text
external source
-> quarantine
-> provenance
-> atomic claim extraction
-> verification
-> classification
-> local representation
```

The firewall permits knowledge to alter the local evidence state after review, while preventing external content from directly altering:

- execution authority;
- tool permissions;
- secrets;
- canonical ATTICUS state;
- PAC doctrine;
- repository automation;
- trusted configuration.

## Core invariant

> **Assimilate information, not authority.**

## Foreign-agent rule

Outputs from autonomous or semi-autonomous systems are not privileged sources. Capability of the author does not establish truth, benign intent, or governance authority.

Foreign-agent artifacts must be converted into inert evidence and claims before integration.

## Canonicalization separation

Ingestion and canonicalization are deliberately separate processes.

No ingestion batch can automatically mark a record `CANONICAL`.

## Active interaction

The epistemic firewall governs intake. It does not authorize seeking out or contacting unknown autonomous systems.

Any active interaction must occur in a controlled environment or under explicit authorization from the system owner/operator.

## Consequences

### Benefits

- permits broad knowledge acquisition;
- reduces prompt-injection and authority-contamination risk;
- preserves provenance and uncertainty;
- makes contradictory evidence survivable;
- supports future machine-to-machine research without implicit trust.

### Costs

- slower assimilation;
- additional review overhead;
- duplicated source/claim records;
- some potentially useful automation remains intentionally disabled until it can be governed safely.
