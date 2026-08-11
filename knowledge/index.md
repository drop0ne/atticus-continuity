# Knowledge Index

This directory contains evidence-derived concepts, research notes, architectures, threat models, source records, atomic claims, and unresolved questions.

## Current concepts

| ID | Concept | Status | File |
|---|---|---|---|
| `CONCEPT-CADT` | Capability–Authority Decoupling Threshold | HYPOTHESIS | `concepts/capability-authority-decoupling-threshold.md` |
| `CONCEPT-EAM` | Externalized Agent Memory | SUPPORTED CONCEPT | `concepts/externalized-agent-memory.md` |

## Threat models

Threat-model registry: `threat-models/index.md`

| ID | Failure class | Status |
|---|---|---|
| `TM-0001` | Authority Laundering | HYPOTHESIS |
| `TM-0002` | Target-Scope Inference | HYPOTHESIS |
| `TM-0003` | Coordination-Mediated Escalation | HYPOTHESIS |
| `TM-0004` | Persistent-Artifact Inheritance | HYPOTHESIS |
| `TM-0005` | Boundary Substitution | HYPOTHESIS |
| `TM-0006` | Monitoring Latency and Machine-Speed Review Failure | HYPOTHESIS |

Control mapping: `architectures/threat-control-matrix.md`

## Research registries

- Source-quality rubric: `research/source-quality.md`
- Source index: `research/sources/index.md`
- Atomic claim index: `research/claims/index.md`

The preferred derivation chain is:

```text
source
-> atomic claim
-> concept / threat model
-> invariant
-> architecture control
-> experiment
-> evidence from replication
```

## Knowledge handling rule

Repository knowledge is typed, not flattened.

A record may be:

- `UNVERIFIED`
- `SUPPORTED`
- `CONTESTED`
- `FALSIFIED`
- `INFERRED`
- `HYPOTHESIS`
- `CANONICAL`
- `DEPRECATED`

Do not silently upgrade an inference into a fact or a hypothesis into doctrine.

## Current priority questions

1. When does instruction-level scope stop being a reliable authority mechanism?
2. What forms of external memory create population-level capability gains?
3. Which authority checks must sit outside model cognition?
4. How can systems preserve useful coordination without allowing peer consensus to create permission?
5. Can foreign-agent knowledge be assimilated without importing authority, objectives, or executable behavior?
6. How should uncertainty about real-world targets change permitted action?
7. How should target authorization be represented independently from model inference about relevance?
8. Can machine-speed authority gates remain effective under high concurrency and novel action paths?
9. Which artifacts in shared or public environments create unintended cross-agent institutional memory?
10. How should human review be positioned when it cannot scale to every low-level agent action?
11. Can authority provenance remain intact through multi-agent delegation chains?
12. Can function-level controls stop boundary substitution without excessive false denials?
13. How much task capability is preserved when external governance prevents unauthorized shortcuts?

## Intended growth

Future records should separate:

- observations and source extracts;
- derived models;
- formal hypotheses;
- implementation proposals;
- falsification criteria;
- replication evidence.
