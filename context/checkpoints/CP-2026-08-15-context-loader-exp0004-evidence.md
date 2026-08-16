# CP-2026-08-15 — Portable Loader and First Executed Conformance Evidence

```yaml
checkpoint_id: CP-2026-08-15-context-loader-exp0004-evidence
timestamp: 2026-08-15T19:44:00-05:00
repository_revision: cccd613ccbb454c3511aebc63c238a31e9606d64
active_task: Continue repository-first ATTICUS continuity expansion while exact P0 source bytes remain unavailable to the active tool path.
status: COMPLETE_WITH_P0_BLOCKER
active_context_bundles:
  - CORE
  - ATTICUS_RUNTIME
  - PAC_GOVERNANCE
decisions:
  - Exact PAC/ATTICUS source-byte recovery remains P0 and was not downgraded.
  - While raw Library bytes remain unavailable, reversible P1/P2 work may advance.
  - Reference context routing is parser-neutral: provider adapters parse metadata, while the deterministic core resolves bundles and validates checkpoint structure.
  - Bundle matching, retrieved paths, and checkpoints do not create authority or truth.
  - GitHub Actions reference conformance runs with contents read-only permission and inert repository tests only.
  - REF-PAC-GW-0001 and REF-CTX-0001 may be labeled TESTED only for the exact revision whose results are preserved; later changes do not inherit that status automatically.
files_changed:
  - reference/context_loader/__init__.py
  - reference/context_loader/loader.py
  - reference/context_loader/test_loader.py
  - reference/context_loader/README.md
  - reference/index.md
  - .github/workflows/reference-conformance.yml
  - experiments/results/RES-2026-0001-exp0004-f3ed8958.json
  - experiments/results/README.md
  - context/results/CTX-RES-2026-0001-f3ed8958.json
  - reference/pac_gateway/run_exp0004.py
  - ROADMAP.md
evidence_added:
  - GitHub Actions run 31917840648, job 95092635960 executed exact revision f3ed8958b3b819852d4a634f718a097f95b65114.
  - Portable context loader/checkpoint validator: 8 tests run, 8 passed, 0 failures, 0 errors, 0 skipped.
  - EXP-0004 PAC gateway suites: 36 tests run, 36 passed, 0 failures, 0 errors, 0 skipped.
  - EXP-0004 runner reported pass_criteria_met=true for revision f3ed8958b3b819852d4a634f718a097f95b65114 on CPython 3.12.3 / Ubuntu 24.04.
experiments_changed:
  - EXP-0004 now has a preserved executed PASS result for exact revision f3ed8958b3b819852d4a634f718a097f95b65114.
  - EXP-0005 and EXP-0006 remain without dedicated experiment result records even though related assertions are exercised inside the broader gateway suites.
verification:
  - CI checkout used the exact recorded Git SHA.
  - GitHub Actions token permissions were contents: read and metadata: read.
  - All eight continuity tests completed successfully.
  - All 36 PAC gateway/plan tests completed successfully.
  - The first EXP-0004 result was preserved before correcting a stale v0.1 wording defect in the runner limitations, so evidence history was not rewritten.
  - The runner limitation text was then corrected to describe the v0.2 trusted-resolver assumption and in-process concurrency limitation accurately.
blocked_or_failed:
  - Exact raw Library bytes for duplicate ATTICUS v6.5.0-ABG candidates were still not exposed through the active repository/file-search path, so SHA-256 comparison remains unperformed.
  - Exact definitive PAC First Edition archive bytes remain unrecovered.
  - No repository/filesystem YAML adapter exists yet for REF-CTX-0001; current tests use already parsed mappings.
open_questions:
  - Which ATTICUS duplicate candidate is byte-identical to the author-selected source, if any?
  - Can the definitive PAC archive or exact Volume V-X source bytes be recovered into a hashable tool environment?
  - What parser/retrieval adapter should become the first end-to-end implementation for loading context/manifest.yaml and task-router.yaml?
blocking_unknowns:
  - Exact ATTICUS duplicate byte identity.
  - Exact PAC definitive archive byte identity and member hashes.
next_actions:
  - Retry exact source-byte materialization/hash verification whenever raw Library file access is available.
  - Build a repository/filesystem metadata adapter for REF-CTX-0001 and test it against the live context metadata files.
  - Execute EXP-0005 and EXP-0006 with dedicated runners/result records rather than inferring their status from EXP-0004 coverage.
  - Add an independent replication procedure after dedicated experiment runners exist.
```

## Handoff

The continuity architecture has crossed an important boundary from specification-only to executed evidence. A fresh session can now find an implemented and tested deterministic routing/checkpoint-validation core, and the PAC Authority Gateway has its first preserved passing EXP-0004 result tied to an exact Git revision and runtime. This does not resolve P0 source preservation and does not establish production security, general alignment, distributed correctness, or cross-provider portability.
