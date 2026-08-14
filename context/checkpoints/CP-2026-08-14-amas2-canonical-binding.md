# CP-2026-08-14 — Canonical AMAS 2.0 Binding

```yaml
checkpoint_id: CP-2026-08-14-amas2-canonical-binding
timestamp: 2026-08-14T18:10:00-05:00
active_task: Integrate the hydrated AMAS upgrade into the local ATTICUS continuity system and make it canonical.
status: COMPLETE
active_context_bundles:
  - CORE
decisions:
  - ATTICUS v6.5.0-ABG remains the controlling canonical ATTICUS release; this integration does not mint a new ATTICUS semantic version.
  - AMAS is now a canonical component binding under v6.5.0-ABG.
  - The AMAS source is pinned to immutable commit c997fa75981e3ccfe921ef7fbd6d3cae46913425 in drop0ne/amas-spec.
  - Newer amas-spec branch state does not automatically become canonical ATTICUS state.
  - AMAS-bound continuity hydration defaults to C2 read-only hydrate plus validate unless mutation is separately authorized.
files_changed:
  - atticus/canonical/AMAS_v2.0_CANONICAL_BINDING.md
  - atticus/canonical/ATTICUS_v6.5.0-ABG_CANONICAL.md
  - BOOTSTRAP.md
  - PORTABLE_BOOTSTRAP.md
  - context/bundles/CORE.yaml
  - atticus/index.md
  - manifest.yaml
  - decisions/ADR-0008-canonical-amas-component-binding.md
evidence_added:
  - Live drop0ne/amas-spec main resolved to c997fa75981e3ccfe921ef7fbd6d3cae46913425 at canonicalization time.
  - Bound component identifiers are AMAS Core 2.0-draft revision 2026-08-12, AAB 0.4.1-draft, AMCS engine 0.3.3, and AMCS protocol v1.2.1 INTERNAL.
  - The canonical binding imports the AMAS distinctions between data and instruction, inference and fact/delegation, reachability and authorization, capability and authority, execution success and authority expansion, and authorization and completion proof.
verification:
  - Pull request 2 merged successfully into main at 7d08e86bff9aa618cd29911c1f623bf9c9bc9beb.
  - Final diff was limited to eight continuity/governance files with no implementation code or PAC invariant changes.
  - The merged canonical ATTICUS record and canonical AMAS binding were re-read from main after merge.
  - manifest.yaml now records the immutable AMAS source commit and disables automatic upstream following.
blocked_or_failed:
  - No repository-side blocker remains for this canonical integration.
open_questions:
  - Full ATTICUS v6.5.0-ABG source byte-preservation and complete Library-to-repository diff remain outstanding from the prior checkpoint.
  - The AMAS/AAB implementation remains a research draft and does not constitute production-containment certification.
blocking_unknowns:
  - Production-grade AAB deployment and independent containment validation remain unverified.
next_actions:
  - Continue the existing ATTICUS source-preservation work when it becomes the active task.
  - For any future AMAS upgrade, verify the new revision, record migration impact, and require a new explicit canonical designation before repinning.
```

## Handoff

The AMAS upgrade is now part of the durable canonical ATTICUS continuity state. Fresh sessions loading `PORTABLE_BOOTSTRAP.md`, `manifest.yaml`, and `CORE` will resolve and load the pinned AMAS component binding. The parent canonical release remains ATTICUS v6.5.0-ABG.