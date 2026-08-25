# CP-2026-08-25 — Exact-Revision Conformance Evidence

```yaml
checkpoint_id: CP-2026-08-25-exact-revision-conformance-evidence
timestamp: 2026-08-25
active_task: Preserve exact-revision execution evidence after ATTICUS raw-byte recovery remained blocked.
status: COMPLETE_FOR_C4975992
active_context_bundles:
  - CORE
  - ATTICUS_RUNTIME
  - PAC_GOVERNANCE
source_state:
  atticus:
    markdown_candidates: 2
    docx_candidates: 2
    indexed_text_agreement: SUPPORTED
    raw_byte_access: UNAVAILABLE_ON_CURRENT_FILE_LIBRARY_SURFACE
    exact_byte_identity: UNRESOLVED
  pac:
    definitive_member_set: RECOVERED_AND_HASHED_LOCAL
    exact_raw_tar_repository_blob: PENDING_BINARY_CAPABLE_TRANSPORT
verification_source:
  revision: c497599284e317549d3b2496383cf1b8a3c06507
  workflow_name: Reference Conformance
  workflow_run_id: 32677079145
  workflow_run_number: 61
  job_id: 97287077506
  event: push
  conclusion: success
  runtime:
    os: Ubuntu 24.04.4 LTS
    python: 3.12.3
    git: 2.55.0
  token_permissions:
    contents: read
    metadata: read
results:
  continuity_suite:
    tests: 34
    failures: 0
    errors: 0
    skipped: 0
    result: PASS
    includes:
      - portable context loader and checkpoint validator
      - fail-closed checkpoint writer
      - filesystem metadata adapter
      - provider-conformance evidence validator
  source_integrity_suite:
    tests: 10
    failures: 0
    errors: 0
    skipped: 0
    result: PASS
  pac_gateway_suite:
    tests: 46
    failures: 0
    errors: 0
    skipped: 0
    result: PASS
  exp0004:
    tests: 36
    pass_criteria_met: true
  exp0005:
    tests: 10
    pass_criteria_met: true
  exp0006:
    tests: 10
    pass_criteria_met: true
preserved_evidence:
  - reference/results/REF-CONFORMANCE-2026-0001-c4975992.json
roadmap_effect:
  - exact-revision checkpoint-writer evidence complete
  - exact-revision filesystem-adapter evidence complete
  - exact-revision provider-conformance-validator evidence complete
  - exact-revision source-integrity-verifier evidence complete
limitations:
  - Evidence applies only to c497599284e317549d3b2496383cf1b8a3c06507; later changed implementations require new runs.
  - Provider validator PASS is not a named-provider CPBC-01..12 execution.
  - Source-integrity PASS does not hash ATTICUS candidates because their raw bytes remain inaccessible through the current File Library surface.
  - PAC gateway tests use inert/synthetic fixtures and do not establish production security or general alignment.
files_changed:
  - reference/results/REF-CONFORMANCE-2026-0001-c4975992.json
  - reference/index.md
  - ROADMAP.md
  - context/checkpoints/CP-2026-08-25-exact-revision-conformance-evidence.md
  - context/LATEST.md
next_priority:
  - Retry exact ATTICUS v6.5.0-ABG raw-byte recovery and hash/compare immediately when a byte-capable source path exists.
  - If still blocked, implement the remaining provider adapters and execute the first named-provider CPBC run, or add the independent replication procedure for existing inert experiments.
```

## Handoff

The major exact-revision evidence debt in the existing continuity implementation is now closed for `c4975992`. Raw-source preservation, especially ATTICUS candidate byte access and exact PAC TAR repository transport, remains the controlling P0 limitation.
