# Provider Adapters

Provider adapters translate repository-first continuity into the capabilities exposed by a specific AI platform or local runtime.

They do **not** redefine ATTICUS, PAC, canonical state, or repository authority. A provider adapter is an integration layer around the portable bootstrap and hydration policy.

## Files

- `TEMPLATE.md` — required structure and conformance expectations for new adapters.
- `chatgpt.md` — current ChatGPT/OpenAI working adapter.
- future provider-specific adapters live beside these files.

## Status model

- `PLANNED` — adapter not yet specified.
- `WORKING` — usable specification exists but complete provider conformance evidence is not preserved.
- `TESTED` — executed evidence exists for a named provider/runtime version and date.
- `DEPRECATED` — retained for history but not the active integration path.

Provider behavior changes over time. `TESTED` therefore applies only to the verified provider/runtime conditions recorded with the evidence.

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
