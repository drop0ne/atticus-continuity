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
- [x] Resolve PAC Volumes V–X existence/status from primary session record
- [x] Recover operator-designated definitive PAC First Edition TAR payload with 24 members
- [x] Calculate SHA-256 for the recovered TAR and all 24 members
- [x] Resolve Appendix F physical filename as `RED_TEAM_ASSESSMENT_PAC.docx`
- [x] Preserve machine-readable PAC archive/member integrity manifest in repository
- [ ] Mirror the exact 931,840-byte PAC TAR blob through a binary-capable GitHub transport and verify repository-retrieved SHA-256
- [ ] Locate/verify the exact historical `.tar.gz` wrapper if it still exists; wrapper recovery is lineage-only and does not block use of the recovered definitive member set
- [x] Deterministically extract and hash PAC source-text projections from all definitive DOCX/SVG members without editorial rewriting
- [x] Build stable PAC source/chapter index mapped to definitive member and text-projection hashes
- [ ] Mirror the complete per-member PAC UTF-8 projection set into GitHub and verify projection hashes
- [ ] Hash and compare standalone pre-definitive PAC candidates where useful for lineage
- [ ] Hash and compare ATTICUS v6.5.0-ABG full-stack candidates
- [ ] Diff Library ATTICUS Markdown against repository canonical representation
- [ ] Preserve complete canonical ATTICUS v6.5.0-ABG source with verified completeness
- [x] Build stable ATTICUS source-section/module index
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
- [x] Build provider-neutral context manifest v0.6
- [x] Define provider-neutral hydration policy
- [x] Build reference context loader
- [x] Build structural checkpoint validator
- [x] Execute and preserve initial context-loader/validator test evidence
- [x] Build fail-closed checkpoint writer with explicit write enablement, exclusive create, and compare-and-swap `LATEST.md` update
- [x] Preserve exact-revision executed checkpoint-writer conformance evidence (`c4975992`, run 32677079145)
- [x] Add repository/filesystem metadata adapter for the reference loader
- [x] Preserve exact-revision executed filesystem-adapter conformance evidence (`c4975992`, run 32677079145)
- [x] Add provider adapter template and provider-adapter status model
- [x] Add Claude adapter
- [ ] Add Gemini adapter
- [x] Add local OpenAI-compatible adapter
- [ ] Add llama.cpp/Ollama-style adapter
- [x] Create cross-provider bootstrap conformance suite
- [x] Preserve exact-revision executed validator evidence for the cross-provider conformance suite (`c4975992`, run 32677079145)
- [ ] Execute ChatGPT adapter under CPBC-01 through CPBC-12 and preserve named-provider evidence
- [ ] Execute Claude adapter under CPBC-01 through CPBC-12 and preserve named-provider evidence
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
- [x] Source hash verification command (`REF-SRC-INT-0001`)
- [x] Preserve exact-revision source-integrity verifier execution evidence (`c4975992`, run 32677079145)
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

PAC P0 materially advanced again on 2026-08-26. The definitive 24-member TAR remains the controlling source package. All 23 DOCX members and the SVG were deterministically projected to UTF-8 locally without editorial rewriting; two independent extraction runs produced the same aggregate projection-tree digest `a2cb235fb5a1ab5da3e89a40e85a25e861f061b82609151fbe46ec61d41a1715`. Stable chapter-index shards now map logical members to definitive source SHA-256 values, text-projection SHA-256 values, observed Heading-style structure, and numbered-label observations. The indexes preserve source irregularities rather than silently repairing them.

The remaining PAC preservation gaps are transport rather than source identification: the exact 931,840-byte TAR and complete 644,507-byte projection tree are still not repository-mirrored through the current connector. Recovery of the historical gzip wrapper remains a lineage question rather than a blocker for the definitive 24-member source set.

ATTICUS remains the main unresolved source-recovery problem: two Markdown and two DOCX v6.5.0-ABG full-stack candidates are known and continue to agree in indexed text, but exact duplicate byte comparison and complete repository/source diff remain outstanding because the current File Library surface still does not expose raw bytes. `REF-SRC-INT-0001` supplies the deterministic read-only SHA-256/size verification command needed immediately when raw bytes become accessible; indexed text does not count as byte identity.

Exact-revision evidence debt for the checkpoint writer, filesystem metadata adapter, provider-conformance evidence validator, and source-integrity verifier was closed for revision `c497599284e317549d3b2496383cf1b8a3c06507` by GitHub Actions run `32677079145`: 34 continuity tests, 10 source-integrity tests, and 46 PAC gateway tests passed with zero failures/errors/skips under Python 3.12.3 / Ubuntu 24.04.4. The result is exact-revision only and does not constitute named-provider CPBC execution or production-security evidence.

The provider-neutral adapter layer is registered in context manifest v0.6. ChatGPT, Claude, and local OpenAI-compatible adapters are `WORKING`; the immediate P1 backlog is Gemini and llama.cpp/Ollama adapters plus first named-provider CPBC runs.

The immediate P2 experiment backlog is independent replication procedure + broader multi-agent sandbox scenarios; EXP-0004, EXP-0005, and EXP-0006 have preserved executed PASS evidence for exact recorded revisions only.

Growth is measured by recoverability, evidence quality, portability, falsifiability, implementation quality, and safety—not repository size.
