# CP-2026-08-14 — Portability Bundles and Hydration Policy

```yaml
checkpoint_id: CP-2026-08-14-portability-bundles
timestamp: 2026-08-14T19:42:24-05:00
active_task: Continue repository-first ATTICUS continuity expansion after canonical AMAS binding.
status: COMPLETE_WITH_P0_BLOCKER
repository_revision: 57e01a9be29778510ae91199fedff6a0f561215c
active_context_bundles:
  - CORE
  - ATTICUS_RUNTIME
  - PAC_GOVERNANCE
decisions:
  - Exact ATTICUS/PAC byte preservation remains P0 and was not downgraded.
  - Current Library search confirms two Markdown and two DOCX ATTICUS v6.5.0-ABG full-stack candidates, but the active tool path did not expose raw Library bytes for SHA-256 computation.
  - Sampled textual equivalence remains evidence of textual agreement only and is not promoted to byte identity.
  - While raw-byte recovery is blocked, reversible P1 portability work may advance without weakening source-verification requirements.
  - ATTICUS_RUNTIME and PAC_GOVERNANCE are now active task-specific bundles.
  - Hydration uses minimum sufficient context and treats bundle routing as retrieval metadata, never authority.
files_changed:
  - context/bundles/ATTICUS_RUNTIME.yaml
  - context/bundles/PAC_GOVERNANCE.yaml
  - context/hydration-policy.md
  - context/manifest.yaml
  - ROADMAP.md
evidence_added:
  - Library search again resolved the two ATTICUS_v6_5_0_ABG_FULL_STACK.md candidates and two DOCX candidates already recorded in the ATTICUS source map.
  - Repository invariant directory was checked and confirms the PAC invariant files referenced by PAC_GOVERNANCE exist on main.
verification:
  - context/manifest.yaml advanced from schema 0.1 to 0.2 and now points to hydration-policy.md.
  - ATTICUS_RUNTIME references the canonical ATTICUS record, canonical AMAS binding, stable source map, and PAC baseline.
  - PAC_GOVERNANCE separates governance/invariants/architecture from the full PAC book source corpus.
  - ROADMAP marks the two initial task-specific bundles, context manifest v0.2, and provider-neutral hydration policy complete.
blocked_or_failed:
  - Raw Library file bytes were not materialized in this run, so SHA-256/byte-size comparison of the four ATTICUS candidates remains unperformed.
open_questions:
  - Which of the duplicate ATTICUS source files is byte-identical to the author-selected source, if any?
  - When will the exact definitive PAC First Edition archive or exact V-X source bytes become retrievable for hashing and preservation?
blocking_unknowns:
  - Exact ATTICUS duplicate byte identity.
  - Exact PAC definitive archive byte identity and member hashes.
next_actions:
  - Retry exact source-byte materialization/hash verification when a raw-file path is available.
  - Otherwise build the reference context loader and checkpoint validator against context manifest v0.2.
  - Then execute inert EXP-0004/5/6 suites against exact repository revisions and preserve results.
```

## Handoff

Fresh sessions now have two useful non-CORE retrieval bundles and a provider-neutral hydration policy. This materially reduces the need to load the entire framework for ATTICUS/PAC governance work while preserving the distinction between routing/index metadata and exact source text. P0 source-byte verification remains unresolved and must not be inferred from sampled text agreement.
