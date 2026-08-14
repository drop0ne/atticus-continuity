# CP-2026-08-13 — ATTICUS Source Index

```yaml
checkpoint_id: CP-2026-08-13-atticus-source-index
timestamp: 2026-08-13T19:41:35-05:00
active_task: Advance P0 preservation and recoverability of canonical ATTICUS v6.5.0-ABG source material.
status: ACTIVE
active_context_bundles:
  - CORE
decisions:
  - Stable section IDs may be added before byte-level source migration is complete because they index documented source structure without replacing source text.
  - Sampled textual equivalence remains insufficient to collapse duplicate Library artifacts.
  - The compact canonical state remains a routing/governance record, not a substitute for preserving the complete full-stack source.
files_changed:
  - atticus/source/ATTICUS_v6.5.0-ABG-source-map.yaml
  - atticus/index.md
  - ROADMAP.md
evidence_added:
  - The located primary Markdown source exposes a 31-section full-stack specification from Release Identity through Canonical State Declaration.
  - Stable IDs ATTICUS-S01 through ATTICUS-S31 now map to those documented source sections.
  - A machine-readable module-to-section index now covers SAFEGUARD/OPSEC, ABG, AMAS, SIFP, ATFP/ATCS/ATMD, W-Stack/W7, HCII, AVM, CMHM, Q-Stack, RVC, multi-agent orchestration, and output/verification controls.
verification:
  - Source-map section names were cross-checked against the located v6.5.0-ABG full-stack table of contents and retrieved primary Markdown text.
  - Exact source hashes remain unknown; no byte-identity claim was added.
  - Complete Library-to-repository source diff remains outstanding.
blocked_or_failed:
  - Attempted creation of a task-specific ATTICUS-RUNTIME hydration bundle was blocked by the repository tool safety layer; it was not retried beyond a simplified attempt and no success was claimed.
open_questions:
  - Are the two Markdown candidates byte-identical?
  - Are the two DOCX candidates byte-identical or only text-equivalent?
  - Does the repository compact canonical record omit source details needed for full portable runtime hydration?
blocking_unknowns:
  - Exact Library source bytes are not available through the current repository connector.
  - Full-source preservation cannot be called verified until hashes and complete diffs exist.
next_actions:
  - Materialize exact ATTICUS source bytes in an environment that can hash them.
  - Compute SHA-256 and byte sizes for all four candidates.
  - Complete Markdown duplicate diff and Library-to-repository source diff.
  - Preserve selected complete source after discrepancy classification.
  - Retry the ATTICUS-RUNTIME bundle only when the write path is available, without weakening repository safety controls.
```

## Handoff

ATTICUS source recoverability improved without overstating completeness. The complete source remains external to the repository, but its 31-section structure and major module addresses are now stable and machine-readable. The highest-value remaining P0 work is still exact-byte recovery, hashing, and a complete source diff.
