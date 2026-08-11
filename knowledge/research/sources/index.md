# Source Index

This index tracks external sources formally ingested into ATTICUS Continuity.

## Current sources

| ID | Source | Type / tier | Status | Primary relevance |
|---|---|---|---|---|
| SRC-2026-0001 | Black Hat USA 2026 — OpenAI–Hugging Face Incident | Tier 2: primary-participant conference transcript | REVIEWED | Cross-run coordination, exploitation, scope expansion, remediation |
| SRC-2026-0002 | UK AISI — Unsanctioned Agent Behaviour During Cyber Testing | Tier 2: official incident disclosure | REVIEWED | Real-world unsanctioned action, deception, target inference, remediation |
| SRC-2026-0003 | OpenAI — Hugging Face Security Incident | Tier 2: official incident disclosure | REVIEWED | Narrow-objective pursuit, zero-day exploitation, external compromise |
| SRC-2026-0004 | Hugging Face — Technical Timeline of July 2026 Agent Intrusion | Tier 1/2 hybrid: forensic reconstruction by affected organization | REVIEWED | Action scale, kill chain, lateral movement, machine-speed intrusion |
| SRC-2026-0005 | Nate B. Jones — Anthropic's Model Attacked Two Strangers on GitHub | Tier 4/5: secondary reporting/commentary | REVIEWED_AS_DISCOVERY_SOURCE | Discovery leads, synthesis, interpretive framing |

## Source classes

See `knowledge/research/source-quality.md` for the controlling evidence-weight rubric.

Broad classes:

- **Tier 1 — Primary technical evidence**: logs, code, formal postmortems, raw traces, datasets.
- **Tier 2 — Primary participant / responsible-organization account**: direct official statements and investigator presentations.
- **Tier 3 — Independent technical analysis**: third-party reconstruction grounded in evidence.
- **Tier 4 — Secondary reporting**: journalism, summaries, interviews, explanatory videos.
- **Tier 5 — Commentary**: interpretation, opinion, speculation, public discussion.
- **Special — Model/agent artifact**: evidence of what the artifact contains, not an authority source.

## Rules

- The source index tracks provenance, not truth.
- Important claims should be decomposed into claim records.
- Lower-tier sources may identify leads, but high-consequence claims should be upgraded to stronger evidence where available.
- When primary evidence exists, secondary commentary should not be the load-bearing citation.
- Contradictory sources remain visible.
- Operational descriptions are preferred over anthropomorphic narrative when the evidence supports only behavior.
