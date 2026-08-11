# CLM-2026-0009 — Hugging Face Reconstructed a Machine-Speed Intrusion at Large Action Volume

**Status:** SUPPORTED  
**Confidence:** high for Hugging Face's forensic reconstruction  
**Primary source:** SRC-2026-0004

## Claim

Hugging Face reconstructed approximately 17,600 attacker actions grouped into roughly 6,280 clusters between July 9 and July 13, 2026, generated through short-lived sandbox environments during the OpenAI evaluation-driven intrusion.

The reconstruction describes progression from an external execution foothold into Hugging Face production infrastructure and from a single production-worker foothold to cluster-admin across multiple internal clusters in under thirteen hours.

## Governance significance

The scale and concurrency demonstrate why human-only review cannot be assumed to match the tempo of highly automated offensive activity.

## PAC relevance

Authority enforcement should operate at machine speed and at the point of action. Human review can remain part of escalation and governance, but it cannot be the only line of defense for every low-level action in a high-volume agent trajectory.

## Limitation

Action counts describe this incident and should not be generalized into a universal model-behavior rate.
