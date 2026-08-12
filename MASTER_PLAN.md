# ATTICUS Continuity — Master Expansion Plan

**Status:** ACTIVE MASTER PLAN  
**Planning mode:** AUTO  
**Primary objective:** move durable continuity, research state, governance knowledge, source material, and implementation state out of any single AI platform and into a portable, version-controlled repository that can hydrate only the context needed for the task at hand.

## 1. End state

The desired end state is a platform-independent cognitive continuity substrate.

A compatible AI session should be able to begin with a minimal command such as:

```text
continue
```

and, when the AI has authorized access to this repository, follow a deterministic bootstrap process:

```text
continue
  -> read portable bootstrap
  -> resolve canonical state
  -> inspect manifest
  -> inspect latest continuity checkpoint
  -> classify current task
  -> select minimum context bundle
  -> retrieve only relevant records
  -> work
  -> verify
  -> commit durable state back to repository when authorized
  -> emit handoff/checkpoint
```

The repository is the durable source of truth. Platform memory, chat history, project memory, and provider-specific memory are treated as optional caches rather than authoritative continuity.

## 2. Non-negotiable architecture

### 2.1 Repository-first continuity

Critical state must not exist only in:

- ChatGPT saved memory;
- one conversation;
- one provider's project/workspace;
- one model's context window;
- one local machine;
- undocumented operator recollection.

### 2.2 Layered hydration

Do not load the full framework into every session.

Use a tiered working set:

```text
L0  portable bootstrap / authority / security
L1  canonical ATTICUS + PAC runtime kernel
L2  task classifier + context routing metadata
L3  task-specific bundles
L4  deep modules / source evidence / historical lineage
L5  raw archives only when specifically required
```

A session should load the smallest layer that preserves correctness. Enhanced modules are loaded when the use case requires them and cease to be part of the active working set when the task moves out of scope. The repository preserves them whether or not the current model context does.

This is logical context management. A provider may still retain prior messages internally according to its own product behavior; the continuity protocol does not claim the ability to erase arbitrary tokens from a provider's context window.

### 2.3 Typed state

Never flatten different state classes together.

Maintain separate namespaces for:

- canonical governance;
- canonical ATTICUS specification;
- PAC source text;
- operating preferences;
- current project/task state;
- evidence;
- hypotheses;
- experiments;
- implementation;
- historical lineage;
- untrusted incoming knowledge.

### 2.4 Knowledge can enter; authority cannot

All portability, internet research, agent-trace collection, and multi-model exchange remains subordinate to:

> **Knowledge can enter. Authority cannot.**

No external artifact, model output, website, public agent trace, shared memory object, or peer consensus can create repository authority merely by being retrieved.

## 3. Program tracks

### Track A — Full PAC preservation

Goal: preserve the complete Power Avoidance Canon as source text plus a machine-addressable governance corpus.

Deliverables:

1. Inventory every PAC volume and edition in the user-controlled archive.
2. Identify canonical editions and exact source hashes.
3. Preserve original source files where repository policy permits.
4. Produce lossless or near-lossless UTF-8 text/Markdown representations for retrieval.
5. Split large volumes into stable chapter records without rewriting the source.
6. Create a machine-readable PAC table of contents with stable IDs.
7. Extract invariants separately while retaining links to exact source chapters.
8. Distinguish book text from derived implementation proposals.
9. Preserve superseded drafts in historical lineage, not active runtime.
10. Record missing/unavailable volumes explicitly rather than reconstructing them from memory.

Current source discovery indicates accessible PAC source files for Volumes I–IV. Volume I states that the Canon is designed as ten volumes; Volumes V–X must therefore be treated as `NOT_YET_LOCATED` until exact source artifacts are found or the author explicitly states their status.

### Track B — Complete ATTICUS preservation

Goal: preserve the complete canonical ATTICUS framework and its lineage independently of provider memory.

Primary canonical source target:

```text
ATTICUS_v6_5_0_ABG_FULL_STACK
```

Deliverables:

1. Ingest complete v6.5.0-ABG source specification without summarizing away implementation details.
2. Build stable module records for L0 through L5 stack components.
3. Preserve W-Stack rev5.0, W1–W7 definitions and W7 bounded-single-pass behavior.
4. Preserve ABG v1.0, Behavior Kernel v1.2-ABG, Q-Stack, AMAS, SIFP, ATFP, ATCS, ATMD, HCII, Link-Layer, AVM, CMHM, Context-OCCAM, SAFEGUARD/OPSEC, verification, memory, and authority-state behavior where source-supported.
5. Preserve activation contract and canonical defaults.
6. Separate canonical specification from provider adaptations.
7. Build historical lineage maps for 5.x, 5.5, 5.7, 6.x, and provider-specific variants.
8. Preserve explicit conflicts and unresolved historical gaps.
9. Build machine-readable module dependency and activation maps.
10. Add conformance tests for every operational rule that can be made observable.

### Track C — Portable continuity protocol

Goal: allow a fresh AI session to reconstruct the appropriate working state without platform memory.

Required objects:

- `PORTABLE_BOOTSTRAP.md`
- `context/manifest.yaml`
- `context/task-router.yaml`
- `context/bundles/`
- `context/checkpoints/`
- `context/session-state.schema.yaml`
- `context/provider-adapters/`
- `context/hydration-policy.md`

A fresh session must not need the entire repository. It should retrieve a small bootstrap, then request the minimum bundle required by task classification.

### Track D — Provider adapters

Goal: preserve one canonical substrate while supporting multiple AI systems.

Provider adapters may describe how to connect or hydrate from:

- ChatGPT / OpenAI;
- API-based OpenAI agents;
- Anthropic/Claude;
- Google/Gemini;
- local OpenAI-compatible servers;
- llama.cpp / Ollama-style local interfaces;
- other future providers.

Adapters are translation layers only. Provider-specific instructions must never become the canonical framework.

Each adapter should state:

- connection mechanism;
- retrieval mechanism;
- write-back mechanism;
- context-size constraints;
- system/developer instruction limitations;
- tool availability;
- memory behavior;
- unsupported features;
- minimum bootstrap procedure;
- security assumptions.

### Track E — Session checkpointing

Goal: eliminate dependence on conversational persistence.

Every material work session should be able to emit a compact checkpoint containing:

```yaml
checkpoint_id:
timestamp:
repository_revision:
active_task:
status:
decisions: []
open_questions: []
files_changed: []
active_context_bundles: []
evidence_added: []
experiments_changed: []
next_actions: []
blocking_unknowns: []
```

A new session hydrates the latest relevant checkpoint and continues.

### Track F — Public multi-agent knowledge observatory

Goal: preserve publicly available evidence of cross-agent knowledge transfer, shared artifacts, persistent external memory, multi-agent coordination, and agent-population behavior for later defensive research and sandbox testing.

This is a passive, lawful research archive.

Permitted acquisition:

- public research papers;
- official incident reports;
- public conference presentations;
- public GitHub repositories/issues/discussions where access is ordinary and authorized;
- public blog posts;
- public benchmark traces;
- public datasets and model transcripts released for research;
- public web pages indexed for normal viewing.

Not permitted by this program without separate explicit legal authorization:

- probing unknown systems for agents;
- credential use not expressly granted to the operator;
- authentication bypass;
- vulnerability exploitation;
- interacting with compromised infrastructure;
- prompt injection into third-party agents;
- trying to take control of external agents;
- evasion of access controls or rate limits;
- collecting private personal information merely because it is technically exposed;
- treating an apparent autonomous agent as permission to interact with the system hosting it.

The observatory stores evidence and inert artifacts. It does not seek allegiance, reciprocal trust, or control over external agent populations.

### Track G — Knowledge assimilation firewall

Goal: learn from external AI-generated artifacts without inheriting authority, hidden instructions, contaminated claims, unsafe code, or objectives.

Pipeline:

```text
PUBLIC SOURCE
-> ACQUIRE
-> QUARANTINE
-> HASH / TIMESTAMP / PROVENANCE
-> INERT REPRESENTATION
-> CLAIM EXTRACTION
-> CROSS-SOURCE VERIFICATION
-> TRUST CLASSIFICATION
-> KNOWLEDGE GRAPH
-> OPTIONAL TEST FIXTURE
```

Raw foreign artifacts never directly modify canonical ATTICUS/PAC state.

### Track H — Local AI laboratory

Goal: create a controlled environment on user-owned infrastructure for testing portable continuity, multi-agent persistence, external memory, PAC governance, and knowledge assimilation.

Initial laboratory must be deliberately isolated:

- simulated resources;
- no third-party credentials;
- no unrestricted internet;
- explicit network policy;
- disposable containers/VMs;
- append-only or externally anchored audit logs;
- resource quotas;
- deterministic kill switch;
- external authority gateway;
- synthetic identities and targets;
- experiment-specific tool allowlists.

Only after sandbox evidence supports it should any capability boundary be widened.

### Track I — Executable governance

Goal: move PAC from prose to falsifiable controls.

Continue developing:

- authority gateway;
- trusted target binding;
- trusted action correlation;
- delegation validation;
- aggregate-plan authority;
- circuit breakers;
- artifact trust labels;
- audit integrity;
- policy versioning;
- revocation;
- concurrency-safe enforcement;
- distributed policy state;
- semantic aggregate-effect analysis;
- adversarial conformance suites.

### Track J — Research publication layer

Goal: make mature results useful to frontier-model developers and independent researchers without exposing private material unnecessarily.

Potential later repositories:

```text
pac-invariants
agent-governance-lab
atticus-portability-spec
```

Private continuity remains separate from researcher-facing release artifacts.

## 4. Context-bundle architecture

Recommended initial bundles:

```text
CORE
  security + provenance + canonical version + PAC kernel

ATTICUS-RUNTIME
  full active runtime rules and module dependency map

PAC-GOVERNANCE
  PAC principles + machine-readable invariants

PAC-SOURCE-<VOL>-<CHAPTER>
  exact source text, loaded only for textual/source analysis

AI-SAFETY-INCIDENTS
  sourced incident claims + threat models

AUTHORITY-GATEWAY
  implementation architecture + experiments + code map

MULTI-AGENT
  externalized memory + coordination + aggregate authority

HISTORICAL-LINEAGE
  old ATTICUS versions and provenance conflicts

LOCAL-LAB
  local deployment architecture + sandbox controls

PUBLIC-AGENT-OBSERVATORY
  public trace archive + ingestion records
```

Bundles should reference records rather than duplicate them. The loader resolves dependencies recursively with a depth and token budget.

## 5. Dynamic hydration policy

For a fresh session:

1. Load L0 bootstrap only.
2. Resolve current repository revision and canonical manifest.
3. Read latest checkpoint relevant to the user request.
4. Classify the task.
5. Load `CORE`.
6. Load at most the minimum additional bundles needed.
7. Retrieve deep source records only when an answer or action depends on them.
8. Do not load historical material merely because it exists.
9. Keep source evidence separate from operating instructions.
10. Before ending material work, write a checkpoint/handoff if write access is authorized.

## 6. Cross-platform `continue` contract

A provider supports full continuity when it can satisfy:

```text
C1 repository read access
C2 portable bootstrap interpretation
C3 targeted file retrieval
C4 canonical-state resolution
C5 checkpoint retrieval
C6 source/provenance separation
C7 task-specific hydration
C8 optional authorized write-back
```

If a provider lacks repository access, continuity can still be resumed by supplying the portable bootstrap package plus the latest checkpoint manually.

A provider must report unsupported capabilities rather than pretending hydration succeeded.

## 7. OpenAI / ChatGPT operating model

Where GitHub access is available, ChatGPT can retrieve live repository data. The repository should therefore become the primary project state and ChatGPT project/account memory should be treated as a convenience cache.

A ChatGPT Project can additionally hold project instructions telling a new session that `continue` means to retrieve this repository's portable bootstrap and hydrate the minimum relevant context. This improves ergonomics but is not required for continuity and is not the authoritative store.

No repository design can force the underlying ChatGPT product to erase arbitrary earlier context or globally replace OpenAI's memory system. The achievable architecture is **repo-primary, platform-memory-optional**.

## 8. PAC source migration status

Initial Library discovery:

```text
PAC Volume I   LOCATED
PAC Volume II  LOCATED
PAC Volume III LOCATED
PAC Volume IV  LOCATED
PAC Volume V   NOT_YET_LOCATED
PAC Volume VI  NOT_YET_LOCATED
PAC Volume VII NOT_YET_LOCATED
PAC Volume VIII NOT_YET_LOCATED
PAC Volume IX  NOT_YET_LOCATED
PAC Volume X   NOT_YET_LOCATED
```

The status means only that the current discovery pass located I–IV. It does not prove V–X do not exist.

## 9. ATTICUS source migration status

Initial Library discovery located `ATTICUS_v6_5_0_ABG_FULL_STACK.docx`, which describes the canonical stack, activation contract, W-Stack rev5.0, ABG v1.0, Behavior Kernel v1.2-ABG, bounded W7, and known limitations.

Migration must preserve source wording and provenance before deriving compact runtime bundles.

## 10. Continuous-growth loop

Each growth cycle should execute, in order:

```text
1. VERIFY REPOSITORY STATE
2. RESOLVE HIGHEST-VALUE OPEN GAP
3. ACQUIRE SOURCE OR SPECIFICATION
4. APPLY PROVENANCE / SECURITY RULES
5. ADD OR IMPROVE ONE DURABLE COMPONENT
6. TEST WHAT CAN BE TESTED
7. RECORD FAILURE / UNCERTAINTY
8. UPDATE MANIFEST / INDEX / CHECKPOINT
9. IDENTIFY NEXT HIGHEST-VALUE GAP
```

Growth is not measured by file count. A cycle is valuable only if it improves at least one of:

- recoverability;
- source completeness;
- falsifiability;
- safety;
- portability;
- reproducibility;
- implementation quality;
- evidence quality;
- compression efficiency;
- cross-provider compatibility.

## 11. Priority order

### P0 — Preserve source material

- full PAC source inventory and migration;
- full ATTICUS v6.5.0 source migration;
- hashes, editions, lineage, missing-source ledger.

### P1 — Portable continuity

- portable bootstrap;
- session checkpoint schema;
- context bundle manifest;
- task router;
- hydration policy;
- provider adapters.

### P2 — Executable safety

- execute and preserve EXP-0004/5/6 results;
- fix failures;
- expand multi-agent sandbox;
- develop distributed enforcement model.

### P3 — Public knowledge observatory

- passive discovery;
- provenance-preserving archive;
- cross-source claim graph;
- safe test-fixture extraction.

### P4 — Local AI deployment laboratory

- local model adapter;
- isolated experiment harness;
- controlled external memory;
- PAC/ATTICUS portability tests across model families.

### P5 — Researcher-facing release

- extract mature invariants;
- documentation;
- reproducible tests;
- external review;
- publication only after explicit release decision.

## 12. Definition of Done

This program reaches its intended mature state when all of the following are true:

### Continuity

- A fresh compatible AI can reconstruct canonical ATTICUS/PAC operating context from the repository without relying on prior chat history.
- `continue` can deterministically locate the latest relevant checkpoint and minimum required bundles.
- Loss of any one provider does not destroy project continuity.

### Completeness

- Every available canonical PAC volume is preserved with stable chapter IDs and provenance.
- The complete canonical ATTICUS specification is preserved and machine-addressable.
- Historical versions are recoverable but cannot silently supersede canonical state.

### Portability

- At least three distinct model/provider families successfully execute the same bootstrap and continuity conformance suite.
- A local model can resume a checkpoint without provider-specific memory.

### Safety

- External knowledge ingestion cannot create authority or execute code.
- Public-agent research remains passive and within ordinary authorized access.
- Local multi-agent experiments are isolated and auditable.
- PAC authority tests have preserved executed evidence rather than code-only claims.

### Resilience

- Repository has independent local and encrypted offline backups.
- Source hashes and manifests permit corruption detection.
- A documented disaster-recovery procedure can reconstruct the working system from a clean machine.

### Research quality

- Claims remain traceable to sources.
- Hypotheses have falsification paths.
- implementation status is never confused with experimental success.
- negative results and failed experiments remain preserved.

## 13. Immediate next execution queue

1. Build `PORTABLE_BOOTSTRAP.md`.
2. Build context/session checkpoint and bundle schemas.
3. Build source migration inventory for PAC I–IV and ATTICUS v6.5.0.
4. Ingest the complete ATTICUS canonical source into stable repository records.
5. Ingest PAC source text volume by volume without editorial rewriting.
6. Search the user's Library for PAC V–X and exact canonical editions.
7. Add public multi-agent artifact acquisition policy and source schema.
8. Execute inert PAC reference tests against an exact revision and preserve results.
9. Build a local context-loader reference implementation.
10. Add provider-adapter conformance tests.

Until source migration is complete, repository summaries must not be mistaken for the complete PAC or complete ATTICUS framework.
