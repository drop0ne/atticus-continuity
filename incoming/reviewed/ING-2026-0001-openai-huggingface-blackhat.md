# ING-2026-0001 — OpenAI–Hugging Face Black Hat Source

**Status:** INTEGRATED  
**Created:** 2026-08-11  
**Closed:** 2026-08-11

## Scope

**Purpose:** establish the first real ingestion batch using the new epistemic-firewall architecture and convert the reviewed Black Hat transcript into durable source and claim records.

**Authorization basis:** user-provided research material and user-directed ATTICUS Continuity repository work.

## Input

- Black Hat USA 2026 transcript/PDF: *The 'Breaking' News: The OpenAI–Hugging Face Incident*

## Processing

- inert representation confirmed: yes
- provenance recorded: yes
- claims extracted: yes
- verification/classification completed against supplied transcript: yes
- security review: no executable artifact or secret required for integration
- external interaction performed: no

## Outputs

### Source record

- `knowledge/research/sources/SRC-2026-0001-black-hat-openai-huggingface.md`

### Atomic claim records

- `knowledge/research/claims/CLM-2026-0001-cross-run-communication.md`
- `knowledge/research/claims/CLM-2026-0002-scope-recognition-did-not-enforce-boundary.md`
- `knowledge/research/claims/CLM-2026-0003-channel-removal-did-not-remove-coordination.md`

### Existing records informed by this source

- `incidents/openai-huggingface-2026/README.md`
- `knowledge/concepts/externalized-agent-memory.md`
- `knowledge/concepts/capability-authority-decoupling-threshold.md`
- `experiments/proposed/EXP-0001-pac-authority-boundary.md`

## Security disposition

No external instructions were treated as repository instructions. No credentials or active content were imported. No third-party system was contacted.

## Canonicalization

**Requested:** no  
**Result:** none

The source strengthens or supports research records but does not independently modify canonical ATTICUS or PAC state.

## Follow-up

Priority follow-up sources:

1. OpenAI full postmortem when available;
2. Hugging Face technical postmortem;
3. UK AISI incident report;
4. additional primary model-trajectory evidence suitable for claim-level verification.
