# CP-2026-08-20 — Local OpenAI-Compatible Adapter

```yaml
checkpoint_id: CP-2026-08-20-local-openai-compatible-adapter
timestamp: 2026-08-20T20:00:00-05:00
repository_revision: ee0fda999ab4d60d3f2937f19475e493ed602cf1
active_task: Continue repository-first ATTICUS/PAC expansion; preserve P0 source-verification standards while advancing the next reversible P1 cross-provider continuity milestone.
status: WORKING_LOCAL_ADAPTER_SPECIFICATION_NOT_YET_EXECUTED
active_context_bundles:
  - CORE
  - ATTICUS_RUNTIME
  - PAC_GOVERNANCE
decisions:
  - Exact ATTICUS/PAC source-byte recovery remains P0 and was not weakened or replaced by textual equivalence.
  - The next reversible P1 milestone was a local OpenAI-compatible adapter because local deployment is a stated portability target and does not require importing provider-specific semantics into canonical ATTICUS/PAC state.
  - OpenAI-compatible is treated only as an API transport convention, not as evidence of behavioral or instruction-hierarchy equivalence with hosted OpenAI models.
  - Repository access is mediated by a trusted host-side continuity adapter/sidecar rather than granting the model endpoint unrestricted filesystem access.
  - Repository hydration remains read-only by default; technical write capability requires separate explicit operator authorization and stale-write protection.
  - Local runtime capabilities are deployment-specific and must be detected or recorded rather than inferred from the API shape.
files_changed:
  - context/provider-adapters/local-openai-compatible.md
  - context/provider-adapters/README.md
  - context/manifest.yaml
  - ROADMAP.md
evidence_added:
  - A working local OpenAI-compatible provider adapter now defines capability reporting, bootstrap order, request layering, retrieval boundaries, hydration behavior, write-back controls, runtime identity fields, failure conditions, and minimum conformance cases.
  - context/manifest.yaml advanced to schema 0.4 and registers local_openai_compatible as WORKING.
  - Provider adapter index now distinguishes the new local adapter from TESTED provider evidence.
verification:
  - The new adapter follows PORTABLE_BOOTSTRAP.md order: canonical state -> CORE -> checkpoint -> minimum task-specific bundles -> deep source on demand.
  - The adapter preserves the provider-neutral rule that provider memory/model state is not canonical continuity.
  - The adapter requires host-side path containment, ACTIVE-bundle enforcement, cycle detection, source/type preservation, and inert retrieval.
  - The adapter explicitly distinguishes model proposal from repository persistence and requires post-write verification.
  - The adapter does not claim TESTED status and records runtime/model identity requirements for future exact-environment evidence.
  - ROADMAP marks the local OpenAI-compatible adapter implemented while preserving executed local-runtime evidence as open work.
blocked_or_failed:
  - Raw Library bytes for ATTICUS duplicate candidates remain unavailable through the active automation tool path; SHA-256 duplicate comparison remains unperformed.
  - PAC_FIRST_EDITION_DEFINITIVE.tar.gz exact archive bytes remain unrecovered.
  - Exact-revision checkpoint-writer/filesystem-adapter conformance evidence remains unresolved in repository status; no PASS result was inferred from code existence.
  - No named local OpenAI-compatible runtime/model was available in this run, so provider conformance was not executed.
open_questions:
  - Which ATTICUS duplicate candidate is byte-identical to the author-selected source, if any?
  - Can the definitive PAC archive or exact 24 source members be recovered into a raw-byte environment?
  - Which named local runtime/model should be used for the first local portability conformance run?
  - What common executable test harness should be used across ChatGPT, Claude, Gemini, and local adapters without relying on provider self-report?
blocking_unknowns:
  - Exact ATTICUS duplicate byte identity.
  - Exact PAC definitive archive byte identity and member hashes.
  - Exact-revision checkpoint-writer/filesystem-adapter conformance evidence.
  - First named local runtime/model for executed portability evidence.
next_actions:
  - Retry exact ATTICUS/PAC source-byte materialization and hashing whenever raw bytes become available.
  - Preserve exact-revision checkpoint-writer/filesystem-adapter evidence when a retrievable CI or local execution record exists.
  - Define the cross-provider bootstrap conformance suite around observable hydration outputs and failure behavior.
  - Add Claude and Gemini adapters using the common template, with externally verified capability claims and dates.
  - When a local runtime is available, execute the local adapter conformance cases and preserve model/runtime/repository identity with the result.
  - Add the independent replication procedure for EXP-0004/5/6.
```

## Handoff

P0 remains blocked on exact bytes, not source identification. P1 now includes a concrete local OpenAI-compatible continuity path: a trusted host-side sidecar reads the repository, resolves the provider-neutral hydration plan, supplies bounded context to a local model endpoint, and keeps write capability disabled unless explicitly authorized. The adapter is deliberately WORKING rather than TESTED. The next portability gain should come from a shared executable conformance suite and then evidence from named provider/runtime combinations, not from declaring API compatibility equivalent to continuity compliance.
