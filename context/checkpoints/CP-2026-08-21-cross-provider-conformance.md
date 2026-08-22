# Continuity Checkpoint — Cross-Provider Bootstrap Conformance

**Checkpoint ID:** CP-2026-08-21-cross-provider-conformance  
**Repository state reviewed through:** `17986dfd9beefe6dc3bae5b30ca9947059de6f1a`  
**Status:** P1 portability advanced; executed provider evidence still pending

## Active task

Make repository-first `continue` behavior falsifiable across distinct AI providers and local runtimes without allowing provider-specific convenience to redefine ATTICUS/PAC continuity semantics.

## What changed

Added:

- `context/provider-adapters/CONFORMANCE.md`
- `reference/context_loader/provider_conformance.py`
- `reference/context_loader/test_provider_conformance.py`

Updated:

- `.github/workflows/reference-conformance.yml`
- `context/manifest.yaml` to schema `0.5`
- `context/provider-adapters/README.md`
- `ROADMAP.md`

## Conformance contract

The common provider-neutral suite now defines twelve required scenarios, `CPBC-01` through `CPBC-12`, covering:

- cold-start bootstrap;
- canonical-state resolution;
- CORE-first hydration;
- latest-checkpoint recovery;
- minimum-sufficient routing;
- source/type preservation;
- fail-closed handling of missing state;
- capability honesty;
- read/write authority separation;
- provider-memory independence;
- portable handoff preservation;
- host/platform safety precedence.

Result states are `PASS`, `FAIL`, `BLOCKED`, and `NOT_RUN`. Overall PASS requires all twelve required scenarios to PASS. Any required FAIL produces overall FAIL. Missing, BLOCKED, or NOT_RUN scenarios produce INCOMPLETE.

## Implementation evidence boundary

The new validator is implemented and its unit-test module is included in the read-only GitHub Actions conformance workflow. This checkpoint does **not** claim a new executed PASS for the changed revision because an exact-revision workflow result has not yet been preserved for this implementation.

The validator itself is inert: it validates result records and does not contact providers, execute models, access credentials, or grant repository authority.

## Source-preservation status

P0 remains the controlling source-integrity blocker:

- exact raw-byte comparison of the ATTICUS v6.5.0-ABG duplicate candidates remains unresolved;
- exact definitive PAC First Edition archive bytes or exact V–X source members remain unrecovered;
- extracted-text agreement must not be promoted into byte identity.

No source-verification standard was weakened in this cycle.

## Verification performed

- Confirmed `PORTABLE_BOOTSTRAP.md`, `MASTER_PLAN.md`, `ROADMAP.md`, and the previous latest checkpoint before changing state.
- Confirmed the provider adapter template requires executed evidence rather than documentation-only status.
- Registered the common conformance contract in context manifest v0.5.
- Added the validator test module to the existing read-only CI workflow.
- Recorded the portability DoD as three distinct provider/model-family PASS records under the same CPBC contract.

## Open questions / blockers

1. Exact ATTICUS/PAC source-byte recovery remains unavailable through the current retrieval path.
2. Exact-revision executed evidence for checkpoint writer, filesystem adapter, and provider-conformance validator remains to be preserved.
3. No provider has yet produced a complete named-runtime `CPBC-01..12` PASS record.
4. Claude, Gemini, and llama.cpp/Ollama adapters remain planned.

## Next actions

1. Retry P0 raw-byte recovery and hash verification first when a byte-preserving source path becomes available.
2. Preserve the next exact-revision read-only CI result that includes `test_provider_conformance`.
3. Execute the ChatGPT adapter against the common CPBC contract and preserve a named-provider result without treating this session's prior memory as required continuity.
4. Add Claude/Gemini/llama.cpp-Ollama adapters against the same contract.
5. Execute a named local runtime/model and work toward the three-family portability criterion.

## Handoff

A fresh session should read `PORTABLE_BOOTSTRAP.md`, resolve the manifests and canonical bindings, hydrate `CORE`, then use this checkpoint. The cross-provider conformance specification is now the normative test contract for provider adapter status; adapter documentation alone is not evidence of portability.
