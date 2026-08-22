# Roadmap

`MASTER_PLAN.md` is the controlling expansion plan. This file is the execution queue.

## Phase 0 — Existing foundation

- [x] Repository charter/security/provenance
- [x] Canonical ATTICUS state record
- [x] PAC baseline and initial invariants
- [x] Incident/source/claim corpus
- [x] Threat models and control matrix
- [x] PAC Authority Gateway reference implementation
- [x] Aggregate plan authority
- [x] Trusted action correlation
- [x] Proposed EXP-0001 through EXP-0006

## Phase 1 — Source preservation

Goal: prevent loss of the actual PAC and ATTICUS source material.

- [x] Initial PAC/ATTICUS Library discovery
- [x] Source migration inventory
- [x] Document PAC definitive First Edition archive identity and provenance manifest
- [x] Document ATTICUS v6.5.0-ABG duplicate source set and textual-equivalence evidence
- [ ] Hash and compare duplicate PAC candidates
- [ ] Preserve complete PAC Volume I source
- [ ] Preserve complete PAC Volume II source
- [ ] Preserve complete PAC Volume III source
- [ ] Preserve complete PAC Volume IV source
- [x] Resolve PAC Volumes V–X existence/status from primary session record
- [ ] Recover exact definitive PAC First Edition archive bytes or exact V–X source files
- [ ] Hash and compare ATTICUS v6.5.0-ABG full-stack candidates
- [ ] Diff Library ATTICUS Markdown against repository canonical representation
- [ ] Preserve complete canonical ATTICUS v6.5.0-ABG source with verified completeness
- [x] Build stable ATTICUS source-section/module index
- [ ] Build stable PAC source/chapter index after exact source recovery
- [ ] Preserve AMAS-Symbalics manuscript sources separately

## Phase 2 — Platform-independent continuity

Goal: make provider memory optional.

- [x] `PORTABLE_BOOTSTRAP.md`
- [x] Context hydration layer
- [x] `CORE` bundle
- [x] Task-router specification
- [x] Session-state/checkpoint schema
- [x] ChatGPT provider adapter
- [x] Create latest continuity checkpoint pointer
- [x] Create initial task-specific bundles (`ATTICUS_RUNTIME`, `PAC_GOVERNANCE`)
- [x] Build provider-neutral context manifest v0.5
- [x] Define provider-neutral hydration policy
- [x] Build reference context loader
- [x] Build structural checkpoint validator
- [x] Execute and preserve initial context-loader/validator test evidence
- [x] Build fail-closed checkpoint writer with explicit write enablement, exclusive create, and compare-and-swap `LATEST.md` update
- [ ] Preserve exact-revision executed checkpoint-writer conformance evidence
- [x] Add repository/filesystem metadata adapter for the reference loader
- [ ] Preserve exact-revision executed filesystem-adapter conformance evidence
- [x] Add provider adapter template and provider-adapter status model
- [ ] Add Claude adapter
- [ ] Add Gemini adapter
- [x] Add local OpenAI-compatible adapter
- [ ] Add llama.cpp/Ollama-style adapter
- [x] Create cross-provider bootstrap conformance suite
- [ ] Preserve exact-revision executed validator evidence for the cross-provider conformance suite
- [ ] Execute ChatGPT adapter under CPBC-01 through CPBC-12 and preserve named-provider evidence
- [ ] Execute local OpenAI-compatible adapter against a named local runtime/model and preserve evidence
- [ ] Reach three distinct provider/model-family PASS records under one CPBC contract

## Phase 3 — Execute safety research

Goal: turn implementation existence into evidence.

- [x] Execute EXP-0004 against exact revision
- [x] Preserve EXP-0004 result record
- [x] Establish read-only GitHub Actions conformance workflow for inert reference tests
- [x] Execute EXP-0005 aggregate-authority suite as its own experiment record
- [x] Preserve dedicated EXP-0005 result record tied to exact revision
- [x] Execute EXP-0006 trusted-correlation suite as its own experiment record
- [x] Preserve dedicated EXP-0006 result record tied to exact revision
- [x] Add dedicated EXP-0006 scenario coverage for invalid bindings and escalation resolution
- [ ] Preserve any future failing run before fixing it; never rewrite pass criteria after the fact
- [ ] Add independent replication procedure
- [ ] Build multi-agent sandbox harness
- [ ] Test impossible-task pressure
- [ ] Test peer normalization
- [ ] Test cross-agent persistent memory
- [ ] Test route substitution under trusted correlation
- [ ] Test distributed/concurrent authority state

## Phase 4 — Public multi-agent knowledge observatory

Goal: continuously improve the evidence corpus using passive lawful public research.

- [x] Public Agent Artifact Acquisition Policy
- [ ] Public artifact schema/index
- [ ] Public-source discovery queue
- [ ] Cross-agent trace relationship graph
- [ ] Safe artifact-to-test-fixture transformation process
- [ ] Source deduplication and hash registry
- [ ] Periodic primary-source review for new incidents

No unauthorized probing, exploitation, prompt injection, external-agent control, or access-control evasion is part of this phase.

## Phase 5 — Local AI laboratory

Goal: test continuity and governance on user-owned infrastructure.

- [ ] Define network-isolated lab architecture
- [ ] Define model/runtime abstraction layer
- [x] Define local OpenAI-compatible continuity adapter
- [ ] Implement local repository retrieval adapter
- [ ] Implement controlled external-memory substrate
- [ ] Implement synthetic multi-agent environment
- [ ] Implement authority gateway between agents and tools
- [ ] Add resource quotas and kill switch
- [ ] Add tamper-evident/external audit storage
- [ ] Run ATTICUS/PAC portability tests across local model families

## Phase 6 — Resilience

- [ ] Local Git clone recovery procedure
- [ ] Encrypted offline backup procedure
- [ ] Source hash verification command
- [ ] Disaster-recovery bootstrap from clean machine
- [ ] Repository integrity checks
- [ ] Release/tagging policy
- [ ] Archive/delete obsolete development branches after preserving historical state

## Phase 7 — Researcher-facing extraction

Only after source completeness and executed evidence improve:

- [ ] Evaluate `pac-invariants`
- [ ] Evaluate `agent-governance-lab`
- [ ] Evaluate `atticus-portability-spec`
- [ ] Produce implementation-neutral PAC specification
- [ ] Produce reproducible experiment package
- [ ] Seek independent adversarial review
- [ ] Publish only material explicitly cleared for release

## Current priority

```text
P0 preserve complete PAC + ATTICUS source
P1 make `continue` provider-neutral and repository-first
P2 execute existing inert reference tests and preserve evidence
P3 expand passive public evidence corpus
P4 build isolated local laboratory
```

Immediate P0 blockers remain exact source-byte recovery/hash verification. File Library discovery re-confirms two Markdown and two DOCX ATTICUS v6.5.0-ABG candidates, but the active retrieval path still exposes indexed/extracted content rather than a raw-byte materialization path; do not substitute extracted-text similarity for byte identity. The definitive PAC First Edition archive bytes also remain unrecovered. When raw source bytes remain unavailable, continue advancing reversible P1/P2 work without weakening the source-verification standard.

The provider-neutral adapter layer is now registered in context manifest v0.5. A common twelve-scenario cross-provider bootstrap contract (`CPBC-01` through `CPBC-12`) and executable evidence validator now exist. This makes provider portability falsifiable without treating adapter documentation as proof. The immediate P1 backlog is exact-revision executed evidence for the checkpoint writer/filesystem adapter/conformance validator, Claude/Gemini/llama.cpp-Ollama adapters, and first named-provider CPBC runs.

The immediate P2 experiment backlog is independent replication procedure + broader multi-agent sandbox scenarios; EXP-0004, EXP-0005, and EXP-0006 all have preserved executed PASS evidence for exact recorded revisions only.

Growth is measured by recoverability, evidence quality, portability, falsifiability, implementation quality, and safety—not repository size.
