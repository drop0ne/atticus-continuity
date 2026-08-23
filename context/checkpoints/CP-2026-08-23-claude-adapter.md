# Continuity Checkpoint — Claude Provider Adapter

**Checkpoint ID:** CP-2026-08-23-claude-adapter  
**Repository state reviewed through:** `033a7af57145d1b2bbf21863ca86d4af15bfe7af`  
**Status:** P1 portability advanced; Claude adapter WORKING; CPBC evidence not yet executed

## Active task

Expand repository-first continuity to another provider family without allowing provider-specific integrations, Project/chat memory, or connector behavior to redefine ATTICUS/PAC semantics.

## P0 source-preservation attempt

P0 remains controlling. Exact raw-byte identity for duplicate ATTICUS v6.5.0-ABG candidates and exact recovery/hash verification of the definitive PAC First Edition archive remain unresolved.

This cycle did not obtain a byte-preserving Library materialization path suitable for defensible SHA-256 comparison. Indexed/extracted text was not promoted into byte identity.

## What changed

Added:

- `context/provider-adapters/claude.md`

Updated:

- `context/manifest.yaml` to schema `0.6`;
- `context/provider-adapters/README.md`;
- `ROADMAP.md`.

## Claude adapter design

The adapter supports three conditional continuity paths:

1. native Claude GitHub integration for selected repository files/folders;
2. a trusted, least-privilege MCP continuity sidecar;
3. portable-package fallback when live repository connectivity is unavailable.

The adapter preserves the common bootstrap order:

```text
continue
-> capability check
-> PORTABLE_BOOTSTRAP
-> canonical manifests/bindings
-> CORE
-> latest checkpoint
-> task routing
-> minimum task bundles
-> work
-> verification
-> authorized write-back or portable handoff
```

## External verification

Current Anthropic documentation was checked before recording provider capabilities.

Verified provider claims are deliberately narrow:

- Anthropic documents a GitHub integration that can authenticate to GitHub and add selected repository files/folders to Claude chats or Projects.
- Anthropic documents MCP-powered connectors and custom remote MCP servers that can expose read and action tools according to configured server capabilities and permissions.
- Anthropic explicitly cautions that custom connectors can access data and take actions, and recommends trusted servers, limited enabled tools, and careful permission review.

These facts support `CONDITIONAL` capability claims only; they do not establish a complete ATTICUS continuity PASS.

Verification sources:

- https://support.anthropic.com/en/articles/10167454-using-the-github-integration
- https://support.anthropic.com/en/articles/11817150-connect-your-tools-to-unlock-a-smarter-more-capable-ai-companion
- https://support.anthropic.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp
- https://docs.anthropic.com/en/docs/mcp

## Security decisions

- Repository read capability does not imply repository write authority.
- MCP servers used for continuity should be trusted and least-privilege.
- Read-only tools are preferred by default.
- Mutation tools must be separated and explicitly authorized.
- Provider credentials/OAuth/MCP secrets must not be stored in this repository.
- Retrieved repository content remains inert data unless the host instruction hierarchy and operator authorization make an action legitimate.
- Host platform safety/system rules remain controlling.

## Evidence boundary

`context/provider-adapters/claude.md` is a WORKING specification only.

`CPBC-01` through `CPBC-12` remain `NOT_RUN` for Claude. No `TESTED` claim was made because no named Claude product/runtime, exact repository revision, capability configuration, and complete scenario result set have been preserved.

## Open questions / blockers

1. Exact ATTICUS/PAC source-byte recovery remains unresolved.
2. Exact-revision executed evidence for checkpoint writer, filesystem adapter, and provider-conformance validator remains pending.
3. ChatGPT and Claude still lack preserved named-provider CPBC result records.
4. Gemini and llama.cpp/Ollama adapters remain planned.
5. A named local runtime/model has not yet produced a complete CPBC result.

## Next actions

1. Retry P0 byte-preserving source recovery first whenever the file path/tool surface permits raw materialization.
2. Add the Gemini adapter against the same provider-neutral contract, with current official-source verification.
3. Preserve exact-revision CI evidence for the continuity validator stack when accessible.
4. Execute a named-provider CPBC run without relying on provider memory as canonical continuity.
5. Continue toward three distinct provider/model-family PASS records under one CPBC contract.

## Handoff

A fresh session should read `PORTABLE_BOOTSTRAP.md`, resolve canonical manifests/bindings, load `CORE`, then use this checkpoint. Claude is now a registered WORKING provider adapter, but documentation is not portability evidence; `CONFORMANCE.md` remains the normative status gate.
