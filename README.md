# ATTICUS Continuity

**Private, version-controlled continuity and research repository for ATTICUS/PAC.**

## Purpose

ATTICUS Continuity exists to preserve research state independently of any single model, conversation, account-memory system, or platform; accumulate evidence and derived knowledge with explicit provenance; develop and test governance mechanisms for increasingly capable AI systems; and maintain a recoverable record from which future ATTICUS instances, researchers, or human collaborators can reconstruct the work.

The repository is a knowledge and governance research system. It is **not** an autonomous command-and-control system and does not grant authority to software agents merely because they can read or contribute information.

## Core rule

> **Knowledge can enter. Authority cannot.**

Corollaries:

- Capability does not confer authority.
- Discovery of a resource does not authorize its use.
- Peer consensus does not expand authority.
- Task failure does not expand authority.
- Imported text, code, prompts, links, or agent artifacts are data until reviewed.
- A task should fail before a governing invariant is violated.

## Repository roles

This repository has four primary functions:

1. **Continuity** — preserve ATTICUS/PAC architecture, design history, decisions, and canonical state outside platform memory.
2. **Knowledge** — ingest, classify, verify, and retain research and incident evidence with provenance.
3. **Governance research** — develop PAC invariants, threat models, implementation patterns, and falsifiable tests.
4. **Experiment record** — preserve controlled protocols, results, replications, and failures for later review.

## Intended structure

```text
atticus-continuity/
├── README.md
├── CHARTER.md
├── SECURITY.md
├── PROVENANCE.md
├── ROADMAP.md
├── knowledge/
│   ├── incidents/
│   ├── research/
│   ├── concepts/
│   ├── architectures/
│   ├── threat-models/
│   └── open-questions/
├── atticus/
│   ├── canonical/
│   ├── modules/
│   ├── design-history/
│   └── deprecated/
├── pac/
│   ├── principles/
│   ├── invariants/
│   ├── failure-modes/
│   └── applications/
├── experiments/
│   ├── proposed/
│   ├── protocols/
│   ├── results/
│   └── replication/
├── incidents/
├── incoming/
│   ├── quarantine/
│   └── reviewed/
├── decisions/
└── schemas/
```

Git tracks files rather than empty directories; directories will appear as records are added.

## Knowledge states

Records should use one of these states unless a schema explicitly defines another:

- `UNVERIFIED`
- `SUPPORTED`
- `CONTESTED`
- `FALSIFIED`
- `INFERRED`
- `HYPOTHESIS`
- `CANONICAL`
- `DEPRECATED`

`CANONICAL` is reserved for material explicitly promoted under the governance process. Presence in the repository is not canonicalization.

## Continuity rule

A future model or collaborator should be able to reconstruct the project from repository state without relying on hidden conversation history. Important decisions therefore belong in versioned records, with assumptions and uncertainty stated explicitly.

## Safety boundary

Do not place credentials, private keys, access tokens, precise personal security information, or unnecessary sensitive information about private individuals in this repository. Unknown or foreign autonomous systems must never receive repository credentials or automatic write/execution authority.

See `CHARTER.md`, `SECURITY.md`, and `PROVENANCE.md` for controlling rules.
