# CP-2026-08-19 — Provider Adapter Template

```yaml
checkpoint_id: CP-2026-08-19-provider-adapter-template
timestamp: 2026-08-19T19:57:01-05:00
repository_revision: f2ee2f058fcc616deb79a3750a0e47f732fa271b
active_task: Continue repository-first ATTICUS/PAC expansion; preserve P0 source-verification standards while advancing the highest-value reversible P1 portability gap.
status: IMPLEMENTED_SPECIFICATION_AWAITING_PROVIDER_CONFORMANCE_EVIDENCE
active_context_bundles:
  - CORE
  - ATTICUS_RUNTIME
  - PAC_GOVERNANCE
decisions:
  - Exact ATTICUS/PAC source-byte recovery remains P0 and was not weakened or replaced by extracted-text equivalence.
  - The next reversible P1 gap was the absence of a provider-neutral adapter contract for providers beyond ChatGPT.
  - Provider adapters are integration layers only; they do not redefine ATTICUS, PAC, canonical state, or repository authority.
  - Provider memory remains a convenience cache rather than canonical continuity state.
  - Every adapter must explicitly distinguish technical capability, operator authority, repository state, provider memory, and verified persistence.
  - Read-only is the default adapter posture; read capability never implies write authority.
  - Retrieved repository material remains inert data unless the host instruction hierarchy and operator authorization make an action permissible.
files_changed:
  - context/provider-adapters/TEMPLATE.md
  - context/provider-adapters/README.md
  - context/manifest.yaml
  - ROADMAP.md
evidence_added:
  - Provider adapter template now defines identity, capability matrix, bootstrap sequence, retrieval contract, hydration behavior, write-back contract, failure vocabulary, security boundary, and minimum conformance checklist.
  - Provider-adapter README now defines the PLANNED/WORKING/TESTED/DEPRECATED status model and integration-layer separation rule.
  - context/manifest.yaml advanced to schema 0.3 and registers the provider adapter template and index.
verification:
  - Template bootstrap order is consistent with PORTABLE_BOOTSTRAP.md and context/hydration-policy.md.
  - Template requires CORE before task-specific bundles and minimum-sufficient-context retrieval.
  - Template preserves source path and epistemic type and does not treat repository presence as truth or authority.
  - Template requires provider capability reporting rather than simulated unsupported capabilities.
  - Template separates repository read from write capability and requires explicit operator authority before persistence.
  - Template uses existing hydration failure codes and preserves fail-closed semantics.
  - ROADMAP now marks the provider adapter template complete and leaves provider-specific adapters/conformance suite open.
blocked_or_failed:
  - Raw Library bytes for ATTICUS duplicates remain unavailable through the active tool path; SHA-256 comparison remains unperformed.
  - PAC_FIRST_EDITION_DEFINITIVE.tar.gz raw bytes remain unrecovered.
  - No new exact-revision checkpoint-writer/filesystem-adapter CI evidence was retrievable in this run.
  - An attempted machine-readable provider-adapter schema write was blocked by the repository safety layer; the human-readable template was created successfully instead, and no control was bypassed.
open_questions:
  - Which ATTICUS duplicate candidate is byte-identical to the author-selected source, if any?
  - Can the definitive PAC archive or exact 24 members be recovered into a raw-byte environment?
  - Which provider-specific adapter should receive the first executed cross-provider conformance evidence?
blocking_unknowns:
  - Exact ATTICUS duplicate byte identity.
  - Exact PAC definitive archive byte identity and member hashes.
  - Exact-revision checkpoint-writer/filesystem-adapter conformance evidence.
next_actions:
  - Retry raw source-byte materialization/hash verification whenever exact Library bytes become available.
  - Preserve exact-revision context-loader/checkpoint-writer/filesystem-adapter evidence when retrievable.
  - Implement the next provider-specific adapter using context/provider-adapters/TEMPLATE.md without importing provider-specific semantics into the portable core.
  - Define the cross-provider bootstrap conformance suite so adapters can be compared against the same repository-first continuity requirements.
  - Add the independent replication procedure for EXP-0004/5/6.
```

## Handoff

P0 remains blocked on exact source bytes, not source identification. P1 advanced by defining one provider-neutral adapter contract that can be reused for ChatGPT, Claude, Gemini, local OpenAI-compatible runtimes, and llama.cpp/Ollama-style systems. The contract makes provider capability explicit, keeps repository retrieval inert, preserves provenance/type, and requires verified authorization for write-back. The next portability milestone should be provider-specific implementation plus shared conformance evidence rather than another provider-specific narrative built without a common contract.
