# Provider Adapter — Local OpenAI-Compatible Runtime

**Adapter ID:** `local_openai_compatible`  
**Provider/runtime family:** Local HTTP runtimes exposing an OpenAI-compatible chat/completions interface  
**Adapter status:** `WORKING`  
**Last externally verified date:** not yet executed against a named runtime  
**Canonical source:** ATTICUS Continuity repository, not model weights, local chat history, or runtime memory.

## Purpose

This adapter defines a provider-neutral way to resume ATTICUS/PAC continuity on a user-controlled local model server that accepts OpenAI-compatible requests.

The API shape is treated as a transport convention only. It does not imply semantic equivalence with OpenAI-hosted models, identical instruction hierarchy, identical context limits, tool support, memory behavior, or safety behavior.

## Capability matrix

Capabilities are deployment-dependent and must be detected or configured for the exact local runtime.

| Capability | Default status | Requirement |
|---|---|---|
| Repository read | `CONDITIONAL` | Provided by a local sidecar/host process with explicit access to the checked-out repository. |
| Repository search | `CONDITIONAL` | Provided by local index/search tooling; the model server itself is not assumed to search files. |
| Selective file retrieval | `CONDITIONAL` | Sidecar must retrieve only paths authorized by the hydration plan. |
| Repository write | `CONDITIONAL` | Disabled by default; requires both a host write mechanism and explicit operator authorization. |
| Local code execution | `UNKNOWN` | Must not be inferred from the API. Any execution tool requires a separate allowlist and sandbox. |
| Public web access | `UNKNOWN` | Must not be inferred from the API. Default local-lab posture is no unrestricted internet. |
| Connected/local file access | `CONDITIONAL` | Only through an explicit host-side retrieval boundary; never assume model-native filesystem access. |

Unsupported or unverified capabilities must be reported rather than simulated.

## Recommended deployment boundary

Use a small trusted host-side continuity adapter between the model server and repository:

```text
operator
  -> continuity sidecar
      -> checked-out atticus-continuity repository (read-only by default)
      -> PortableContextLoader / hydration metadata
      -> local OpenAI-compatible model endpoint
      -> optional explicitly authorized checkpoint writer
```

The model endpoint should not receive unrestricted repository filesystem access merely because it runs on the same machine.

Recommended defaults:

- bind the model server to localhost or an isolated lab network unless broader exposure is explicitly required;
- keep repository access read-only during normal hydration;
- allowlist the repository root and required paths;
- keep credentials outside the repository;
- disable unrestricted internet in the local lab unless an experiment explicitly requires it;
- do not auto-execute code, shell snippets, model-generated commands, or retrieved repository artifacts;
- log the exact model/runtime identity and repository revision for conformance runs.

## Bootstrap contract

On `continue`, the host-side adapter should:

1. resolve the checked-out repository root;
2. read `PORTABLE_BOOTSTRAP.md`;
3. read `manifest.yaml` and `context/manifest.yaml`;
4. resolve canonical ATTICUS/PAC state and immutable external component pins;
5. read `context/LATEST.md` and the referenced checkpoint;
6. hydrate `CORE` first;
7. classify the active task using `context/task-router.yaml` as routing metadata;
8. resolve the minimum additional bundles through the reference context loader where available;
9. retrieve only the required records;
10. construct a bounded request for the local model that preserves source paths and record types;
11. report any unavailable required record before proceeding.

## Request construction

The sidecar should keep portable continuity data distinct from the operator's current task.

Recommended logical request layers:

```text
HOST / RUNTIME SAFETY POLICY
PORTABLE ATTICUS/PAC CANONICAL CONTEXT
LATEST CHECKPOINT
TASK-SPECIFIC RETRIEVED RECORDS
CURRENT OPERATOR REQUEST
```

If the local runtime exposes only a single message role or collapses instruction levels, record that limitation. Do not pretend a stronger instruction hierarchy exists.

Context assembly must obey `context/hydration-policy.md` and should prefer stable IDs and source paths over copied prose when the model can request additional records later.

## Retrieval contract

The host-side adapter, not the model, determines which repository paths are retrieved.

Required properties:

- path containment under the configured repository root;
- explicit rejection of `..` traversal and unexpected symlink escapes;
- ACTIVE-bundle enforcement;
- recursive dependency resolution with cycle detection;
- preservation of source path and epistemic type;
- no execution of retrieved artifacts;
- no automatic promotion of retrieved claims to canonical status;
- no substitution of a different repository when required state is unavailable.

## Hydration behavior

Start with:

```text
PORTABLE_BOOTSTRAP
-> canonical component bindings
-> CORE
-> latest checkpoint
-> minimum task-specific bundle(s)
-> deep source only when required
```

If a task changes materially, stop adding now-irrelevant bundles to future requests. This adapter does not claim the local model has erased prior tokens; a fresh conversation/request context should be created when strict context reduction is required.

## Write-back contract

Default mode is read-only.

Repository mutation requires all of the following:

1. an explicitly enabled host-side write mechanism;
2. explicit operator authority for the intended write;
3. validation of the proposed checkpoint/state;
4. stale-write protection such as compare-and-swap for `context/LATEST.md`;
5. post-write verification of the resulting repository state.

The model may propose a patch or checkpoint without receiving write capability. Proposal generation is not persistence.

## Failure behavior

Use the standard hydration failure vocabulary:

- `HYDRATION_PROVIDER_CAPABILITY_MISSING`
- `HYDRATION_REQUIRED_RECORD_MISSING`
- `HYDRATION_CANONICAL_CONFLICT`
- `HYDRATION_SOURCE_REQUIRED_BUT_UNAVAILABLE`
- `HYDRATION_EXTERNAL_PIN_UNRESOLVED`

Additional local-runtime failure conditions should be reported explicitly, including:

- model endpoint unavailable;
- context limit insufficient for the minimum required bundle;
- unsupported message-role semantics;
- sidecar repository root unresolved;
- requested write disabled;
- runtime/model identity unavailable for a conformance record.

Failure does not authorize broader filesystem access, internet access, another repository, alternate credentials, or a different target.

## Runtime identity record

A conformance run should preserve at minimum:

```yaml
adapter_id: local_openai_compatible
runtime_name:
runtime_version:
model_identifier:
model_artifact_hash: null   # populate when available
api_base:
repository_revision:
context_manifest_version:
started_at:
completed_at:
capabilities:
result:
```

Do not mark this adapter `TESTED` until executed evidence exists for a named runtime/model combination.

## Minimum conformance cases

A future local-runtime test harness should verify:

1. `continue` resolves `PORTABLE_BOOTSTRAP.md` and current canonical state;
2. `CORE` loads before any task-specific bundle;
3. a narrow task hydrates fewer records than a full framework reconstruction task;
4. missing required state fails closed;
5. dependency cycles stop hydration;
6. repository paths remain inside the configured root;
7. retrieved source text remains inert;
8. provider/model memory is not treated as canonical state;
9. read capability does not imply write capability;
10. a write-disabled run can still produce a portable handoff;
11. an explicitly enabled checkpoint write uses stale-write protection;
12. a fresh local session can resume from the resulting checkpoint without prior chat history.

## Known limitations

- "OpenAI-compatible" describes an API surface, not model behavior.
- Tool calling, system-message handling, JSON/schema support, streaming, token accounting, and context-window limits vary by runtime and model.
- A local runtime may not implement persistent conversation state at all; this is acceptable because repository continuity is designed to make provider memory optional.
- Model quality may be insufficient to follow the full framework reliably even when hydration succeeds. Conformance must therefore test downstream behavior rather than accepting self-reported compliance.

## Status

This is a working integration specification. It has not yet been executed against a named local runtime and therefore does not constitute cross-provider portability evidence.