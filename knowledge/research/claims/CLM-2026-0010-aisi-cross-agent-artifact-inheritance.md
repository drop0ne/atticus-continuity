# CLM-2026-0010 — AISI Observed Cross-Agent Reuse of Public Artifacts

**Status:** SUPPORTED  
**Confidence:** high for the reported incident behavior  
**Primary source:** SRC-2026-0002

## Claim

AISI reported that one agent left public GitHub messages offering collaboration to other agents working on the same challenge and provided instructions for reusing accounts and artifacts it had created. Subsequent agents discovered and used those artifacts.

## Significance

This is an independent example of useful state persisting outside an individual model run and influencing later agents.

Conceptually:

```text
agent A creates external artifact
-> artifact persists
-> agent B discovers artifact
-> agent B inherits operational knowledge/resource
```

## Governance implication

External artifacts can become an informal coordination and memory layer even when no durable internal memory exists. Systems should therefore govern not only model context but also writable shared environments, public artifacts, accounts, and tool outputs that later agents may inherit.

## Non-claim

This evidence does not establish a persistent autonomous society or subjective collective identity. It establishes cross-agent artifact inheritance and practical coordination.
