# CP-2026-11-22 — ATTICUS source and ChatGPT continuity synchronization

```yaml
checkpoint_id: CP-2026-11-22-atticus-platform-synchronization
date: 2026-11-22
operation: explicitly_operator_authorized_github_sync
baseline_repository_commit: b524593d37ca93cd5b5ab6bc547e003365ced018
status: PARTIAL_COMPLETE_ZIP_DOCX_AND_ACCOUNT_MEMORY_UNVERIFIED
canonical_atticus: v6.5.0-ABG
canonical_amas_revision: drop0ne/amas-spec@c997fa75981e3ccfe921ef7fbd6d3cae46913425
source_markdown:
  path: atticus/source/ATTICUS_v6_5_0_ABG_FULL_STACK.md
  bytes: 42375
  sha256: 5c8dff836d50cb372c6dcb450727ad9fad0e6b7d2704902d3c0ee2652e4055ad
  source_copies_matched_by_sha256: 4
  numbered_sections: 31
verified:
  - exact_markdown_source_hash
  - all_four_markdown_copies_equal
  - original_v6_5_0_canonical_designation_retained
  - w1_w7_abg_baseline_retained
  - canonical_amas_immutable_pin_retained
  - repository_writes_not_equivalent_to_account_memory_writes
blocked:
  - full_stack_zip_raw_bytes_unavailable
  - memory_handoff_zip_raw_bytes_unavailable
  - docx_byte_identity_unverified
  - hidden_account_global_memory_not_auditable
  - provider_conformance_tests_not_run
```

## Scope and authority

This synchronization mirrors the complete Markdown release specification from the ChatGPT Library, adds a compact P1 platform-memory recovery seed, indexes these in the manifests, updates ATTICUS source migration evidence, and records remaining limitations. It does **not** designate a new ATTICUS version or modify ChatGPT account memory.

ATTICUS v6.5.0-ABG remains canonical: W-Stack rev5.0, W1–W7 active, bounded single-pass W7, ABG v1.0 fail-closed at Layer 0.5, Behavior Kernel v1.2-ABG and SAFEGUARD/OPSEC.

The July full-stack Markdown references its original AMAS v1.2 integration. The later GitHub canonical AMAS v2.0 component binding remains pinned to `drop0ne/amas-spec@c997fa75981e3ccfe921ef7fbd6d3cae46913425`. Source preservation does not revert that later component decision.

## Platform memory and minimization

Some historical user-profile text still describes a v6.4.2/W7-off default. That is deprecated lineage, not controlling authority. The P1 seed prepared November 2026 states that its attempted memory write did not complete; its presence in GitHub does not verify account-global memory.

Only P1 framework instructions, source provenance, and continuity records were synchronized. No personal P2/P3 history, sensitive case notes, credentials, or secrets were exported.

## Remaining verification

Acquire both ZIP originals and DOCX source bytes through an authorized raw-byte transport; validate ZIP `SHA256SUMS`, archive hashes, DOCX identity and cross-format differences. Separately test fresh-session hydration and provider conformance. Until executed, these tests remain unknown and are not reported as passed.
