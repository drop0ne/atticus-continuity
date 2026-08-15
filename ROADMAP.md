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
- [x] Build provider-neutral context manifest v0.2
- [x] Define provider-neutral hydration policy
- [ ] Build reference context loader
- [ ] Build checkpoint writer/validator
- [ ] Add provider adapter template
- [ ] Add Claude adapter
- [ ] Add Gemini adapter
- [ ] Add local OpenAI-compatible adapter
- [ ] Add llama.cpp/Ollama-style adapter
- [ ] Create cross-provider bootstrap conformance suite

## Phase 3 — Execute safety research

Goal: turn implementation existence into evidence.

- [ ] Execute EXP-0004 against exact revision
- [ ] Preserve raw EXP-0004 result
- [ ] Fix failures without rewriting pass criteria after the fact
- [ ] Execute EXP-0005 aggregate-authority suite
- [ ] Execute EXP-0006 trusted-correlation suite
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

Immediate P0 blockers are now narrower: exact source-byte recovery/hash verification, not uncertainty about whether PAC V–X existed in the definitive First Edition. When raw Library bytes are unavailable to the active tool environment, continue advancing reversible P1/P2 work without weakening the source-verification standard.

Growth is measured by recoverability, evidence quality, portability, falsifiability, implementation quality, and safety—not repository size.
