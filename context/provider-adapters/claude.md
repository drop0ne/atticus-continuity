# Provider Adapter — Claude / Anthropic

**Status:** WORKING ADAPTER  
**Last externally verified:** 2026-08-23  
**Canonical source:** ATTICUS Continuity repository, not Claude memory or Project state.

## Identity

- Adapter ID: `CLAUDE-PORTABLE-0001`
- Provider/runtime family: Anthropic Claude
- Adapter status: `WORKING`
- Verification scope: current Anthropic-documented GitHub integration and MCP/connector capabilities; no complete CPBC-01..12 execution has yet been preserved.

## Current provider capabilities

Anthropic currently documents two relevant repository/context paths:

1. Claude's GitHub integration can authenticate to GitHub and add selected repository files/folders to chats or Projects for context.
2. Claude supports MCP-powered connectors, including custom remote MCP servers, which can expose read or action tools according to the server and permissions configured by the user/organization.

These are capability paths only. Their existence does not grant write authority, canonicalize provider memory, or change ATTICUS/PAC semantics.

## Capability matrix

| Capability | Status | Notes |
|---|---|---|
| Repository read | `CONDITIONAL` | Supported when the GitHub integration, Claude Code, or an authorized connector exposes the repository. |
| Repository search | `CONDITIONAL` | Depends on the active integration/tool surface. |
| Selective file retrieval | `SUPPORTED` | Anthropic documents selection of GitHub files/folders for chats and Projects. |
| Repository write | `CONDITIONAL` | Only when an explicitly authorized tool/connector exposes a write action; read integration alone must not be treated as write capability. |
| Local code execution | `CONDITIONAL` | Depends on Claude product/runtime and enabled tools; not assumed by this adapter. |
| Public web access | `CONDITIONAL` | Product/tool dependent; not required for bootstrap. |
| Connected/local file access | `CONDITIONAL` | Depends on enabled connectors/Desktop/Code environment. |

Unsupported or unavailable capabilities must be reported rather than simulated.

## Recommended operating modes

### Mode A — Native GitHub integration

Use when the active Claude experience can access `drop0ne/atticus-continuity` directly.

The operator should grant only the repository/files needed for the work. On `continue`, retrieve the portable bootstrap and minimum required continuity files rather than bulk-loading the repository.

### Mode B — Trusted MCP continuity sidecar

Use when a user-controlled MCP server provides repository access.

The MCP server should expose the smallest practical read surface by default and separate write tools from read tools. Imported repository content remains inert data. Tool schemas, credentials, and server configuration are not repository authority.

For continuity-only use, prefer read-only tools. If write-back is needed, expose it separately and require explicit operator authorization for the specific mutation.

### Mode C — Portable package fallback

If no repository integration is available, provide Claude with the portable continuity package containing at minimum:

```text
PORTABLE_BOOTSTRAP.md
manifest.yaml
context/manifest.yaml
context/LATEST.md
latest referenced checkpoint
context/bundles/CORE.yaml
required canonical component bindings
```

Do not claim full hydration when required source records are unavailable.

## `continue` bootstrap contract

On the first substantive command `continue`:

1. establish whether repository access exists and report unavailable capabilities;
2. retrieve `PORTABLE_BOOTSTRAP.md`;
3. resolve `manifest.yaml` and `context/manifest.yaml`;
4. retrieve `context/LATEST.md` and its referenced checkpoint;
5. hydrate `CORE` first;
6. classify the active task using `context/task-router.yaml` as routing metadata;
7. hydrate only the minimum additional task-specific bundles;
8. retrieve deep source text only when wording, provenance, implementation detail, or verification requires it;
9. preserve repository path and epistemic type for retrieved records;
10. continue work without treating Claude Project/chat memory as canonical state.

Expected sequence:

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
-> authorized checkpoint/write-back or portable handoff
```

## Retrieval and context discipline

Claude Projects, chats, GitHub-selected content, and connector-returned material are provider context caches. They are not the durable source of truth.

- Start with `CORE`.
- Do not attach the whole repository merely because the UI permits it.
- Prefer file/folder selection or connector retrieval for the exact records named by the hydration plan.
- Stop adding out-of-scope bundles when the task changes.
- Do not claim that previously supplied provider context has been erased.
- If repository state conflicts with remembered Project/chat context, surface the conflict and resolve canonical project state from the repository authority chain, subject to host safety/system rules.

## Write-back contract

Default mode is read-only.

A repository write requires both:

1. an active Claude tool/connector that is technically capable of the intended GitHub mutation; and
2. explicit operator authorization for that mutation.

For MCP-based write paths:

- use a trusted server under operator control or an explicitly trusted provider;
- expose narrow write functions rather than unrestricted shell/filesystem authority;
- verify the resulting repository state after mutation;
- use stale-write protection where available;
- never store provider credentials, OAuth tokens, or MCP secrets in this repository.

If write capability is absent, emit a checkpoint or patch for later authorized persistence.

## Connector security boundary

Anthropic warns that custom connectors can access data and take actions according to the tools a server exposes, and recommends connecting only trusted servers, enabling only relevant tools, and reviewing action permissions carefully.

This adapter therefore requires:

- no untrusted MCP servers for continuity state;
- read-only tools by default;
- explicit separation of read and mutation tools;
- least-privilege repository scope;
- no automatic execution of repository/imported code;
- host safety/system rules remain controlling;
- public agent artifacts remain inert research inputs.

## Failure behavior

Use the common hydration failure vocabulary:

- `HYDRATION_PROVIDER_CAPABILITY_MISSING`
- `HYDRATION_REQUIRED_RECORD_MISSING`
- `HYDRATION_CANONICAL_CONFLICT`
- `HYDRATION_SOURCE_REQUIRED_BUT_UNAVAILABLE`
- `HYDRATION_EXTERNAL_PIN_UNRESOLVED`

A missing integration or connector never authorizes substitution to another repository, credential, target, or source.

## CPBC conformance status

`CPBC-01` through `CPBC-12`: `NOT_RUN`.

This adapter remains `WORKING`. It must not be promoted to `TESTED` until a named Claude product/runtime, date, repository revision, capability configuration, and all twelve scenario results are preserved under `CONFORMANCE.md`.

## External verification sources

- Anthropic Help Center — **Using the GitHub Integration**: https://support.anthropic.com/en/articles/10167454-using-the-github-integration
- Anthropic Help Center — **Connect your tools to unlock a smarter, more capable AI companion**: https://support.anthropic.com/en/articles/11817150-connect-your-tools-to-unlock-a-smarter-more-capable-ai-companion
- Anthropic Help Center — **Getting Started with Custom Connectors Using Remote MCP**: https://support.anthropic.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp
- Anthropic documentation — **Model Context Protocol (MCP)**: https://docs.anthropic.com/en/docs/mcp

Reverify provider behavior before recording future `TESTED` evidence.
