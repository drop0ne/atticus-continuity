# CP-2026-08-24 — Source Integrity Verifier

```yaml
checkpoint_id: CP-2026-08-24-source-integrity-verifier
timestamp: 2026-08-24
active_task: Continue P0 source-preservation work after PAC definitive-source recovery.
status: IMPLEMENTED_LOCAL_TESTED / EXACT_REVISION_CI_PENDING
active_context_bundles:
  - CORE
  - ATTICUS_RUNTIME
  - PAC_GOVERNANCE
source_state:
  pac:
    definitive_tar_payload: RECOVERED_AND_HASHED_LOCAL
    raw_repository_blob: PENDING_BINARY_CAPABLE_TRANSPORT
  atticus:
    markdown_candidates: 2
    docx_candidates: 2
    indexed_text_agreement: SUPPORTED
    exact_byte_identity: UNRESOLVED
    blocker: File Library retrieval still exposes indexed/extracted content rather than raw byte streams.
implementation:
  id: REF-SRC-INT-0001
  path: reference/source_integrity/
  behavior:
    - calculate deterministic SHA-256 and byte size without interpreting artifact content
    - verify one artifact against expected SHA-256 and optional size
    - verify JSON manifests containing relative artifact paths
    - reject malformed digests, duplicate paths, absolute manifest paths, and path traversal outside verification root
    - emit machine-readable JSON result state
    - remain standard-library and read-only
verification:
  local_command: python -m unittest reference.source_integrity.test_verify -v
  local_result: 10 tests passed, 0 failures, 0 errors, 0 skipped
  evidence_boundary: This pre-commit local run validates the staged implementation text but is not exact-revision repository CI evidence.
files_added:
  - reference/source_integrity/__init__.py
  - reference/source_integrity/verify.py
  - reference/source_integrity/test_verify.py
  - reference/source_integrity/README.md
next_repository_updates:
  - index REF-SRC-INT-0001 in reference/index.md
  - add its unit tests to the read-only reference-conformance workflow
  - mark the Phase 6 source-hash verification command implemented in ROADMAP.md
  - advance context/LATEST.md to this checkpoint
open_questions:
  - Can a binary-capable future transport expose the PAC TAR and ATTICUS candidate files as raw bytes for direct verifier execution?
  - Which ATTICUS Markdown/DOCX duplicate bytes are identical, and which exact source should be preserved after hash/diff evidence exists?
next_priority:
  - Preserve exact ATTICUS v6.5.0-ABG source bytes and duplicate hashes as soon as raw-byte access exists.
  - Otherwise preserve exact-revision CI evidence for this verifier and the pending context-loader additions, then continue provider portability work.
```

## Handoff

The source-integrity standard is now executable rather than procedural only. Raw source recovery remains the limiting factor, not the absence of a deterministic verification command.
