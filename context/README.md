# Context Hydration Layer

This directory defines the provider-neutral working-set system used to reconstruct only the context required for the current task.

## Principle

Repository state is durable. Model context is temporary.

```text
durable repository -> selective hydration -> temporary working context -> checkpoint -> durable repository
```

## Objects

- `LATEST.md` — points to the latest general continuity checkpoint.
- `checkpoints/` — durable session/work checkpoints.
- `bundles/` — named context dependency sets.
- `task-router.yaml` — maps task classes to bundles.
- `session-state.schema.yaml` — checkpoint/session-state contract.
- `provider-adapters/` — provider-specific retrieval/write-back instructions.

## Loading rule

Start small. Load `CORE`, then add only the bundles needed for the task. Deep source text should be retrieved on demand rather than permanently copied into every session.

## Unloading rule

The protocol can stop retrieving a bundle when it leaves task scope and can begin a fresh session with a smaller working set. It does not claim control over a provider's hidden context-retention implementation.

## Write-back rule

A model may write repository state only when the provider exposes an authorized write mechanism and the operator has authorized the relevant action. Read access is not write authority.
