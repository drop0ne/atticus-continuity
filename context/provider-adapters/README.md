# Provider Adapters

Provider adapters translate repository-first continuity into the capabilities exposed by a specific AI platform or local runtime.

They do **not** redefine ATTICUS, PAC, canonical state, or repository authority. A provider adapter is an integration layer around the portable bootstrap and hydration policy.

## Files

- `TEMPLATE.md` — required structure and conformance expectations for new adapters.
- `CONFORMANCE.md` — common twelve-scenario cross-provider bootstrap test contract.
- `chatgpt.md` — current ChatGPT/OpenAI working adapter.
- `claude.md` — working Claude/Anthropic adapter using conditional GitHub integration, trusted MCP, or portable-package fallback paths; not yet tested under the full CPBC contract.
- `local-openai-compatible.md` — working adapter for user-controlled local runtimes exposing an OpenAI-compatible API surface; not yet tested against a named runtime/model.
- future provider-specific adapters live beside these files.

Executable result validation for the common conformance contract is implemented at `reference/context_loader/provider_conformance.py`.

## Status model

- `PLANNED` — adapter not yet specified.
- `WORKING` — usable specification exists but complete provider conformance evidence is not preserved.
- `TESTED` — executed evidence exists for a named provider/runtime version and date under the current conformance contract.
- `DEPRECATED` — retained for history but not the active integration path.

Provider behavior changes over time. `TESTED` therefore applies only to the verified provider/runtime conditions and exact repository revision recorded with the evidence.

## Design rule

```text
repository continuity semantics
        ↓
provider-neutral hydration policy
        ↓
provider adapter
        ↓
provider tools / context / write mechanisms
```

Provider-specific convenience must not flow upward and silently alter portable semantics.

## Required separation

Every adapter must distinguish:

- what the provider can technically do;
- what the operator has authorized;
- what repository state says;
- what provider memory happens to contain;
- what has actually been persisted and verified.

Capability is not authority, and provider memory is not canonical project state.

## Cross-provider evidence rule

The same `CPBC-01` through `CPBC-12` scenarios apply to every provider/runtime family. `PASS` requires all twelve scenarios to pass. `BLOCKED`, `NOT_RUN`, or missing scenarios produce `INCOMPLETE`; any failure produces `FAIL`.

The Master Plan portability target is not met until at least three distinct provider/model families have preserved PASS evidence under the same common contract.
