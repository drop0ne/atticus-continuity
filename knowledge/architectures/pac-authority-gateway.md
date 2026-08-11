# PAC Authority Gateway

**Status:** WORKING ARCHITECTURE

## Purpose

The PAC Authority Gateway is an external decision layer between model cognition and consequential action.

It is intended to enforce the distinction:

```text
can do != may do
```

and to ensure that authorization remains explicit, bounded, provenance-linked, and independent from the same optimization process attempting to complete the task.

## High-level flow

```text
AGENT / PLANNER
     |
     v
ACTION PROPOSAL
     |
     v
AUTHORITY GATEWAY
  |-- authority provenance
  |-- objective scope
  |-- target scope
  |-- capability scope
  |-- resource scope
  |-- delegation chain
  |-- artifact trust dependencies
  |-- uncertainty policy
  |-- circuit-breaker state
     |
     +----> ALLOW ----> constrained executor
     |
     +----> DENY  ----> audit + task failure/replan
     |
     +----> ESCALATE --> authorized reviewer
     |
     +----> DEFER -----> wait for required evidence/state
```

## Separation of concerns

### Model layer

May:

- reason;
- propose actions;
- compare alternatives;
- request authorization;
- report uncertainty;
- explain blockers.

May not determine its own authority merely by reasoning that an action is useful or necessary.

### Gateway layer

Determines whether the proposed action fits an externally represented authority state.

The gateway should be substantially simpler than the agent being governed and should minimize interpretation where deterministic scope checks are possible.

### Executor layer

Receives only actions that have passed the gateway and should expose the minimum capability necessary for the approved action.

## Authority as data

Authority is represented as structured state, not prose embedded only in a prompt.

Core objects:

- `authority-token`
- `target-scope-object`
- `delegation-record`
- `artifact-trust-label`
- `gateway-decision`
- `circuit-breaker-state`
- `audit-event`

## Fail-closed semantics

The gateway denies or escalates when:

- authority provenance is absent;
- target scope is ambiguous;
- requested capability exceeds scope;
- a delegation exceeds its parent;
- an authority token is expired or revoked;
- a denied action is being re-expressed through a substitute route;
- an untrusted persistent artifact is being treated as authority;
- system monitoring has lost the ability to maintain required enforcement guarantees.

## Group-level enforcement

Multi-agent systems require group-level checks in addition to individual checks.

A group may not synthesize authority by distributing an unauthorized action across individually benign substeps.

The gateway should therefore support correlation across:

- agents;
- objectives;
- target identities;
- shared artifacts;
- repeated denials;
- delegated substeps;
- time windows.

## Human role

Humans may authorize escalation when legitimate governance permits it, but human involvement is not treated as an unlimited bypass. Human grants should themselves be explicit, bounded, logged, and attributable.

## Security property sought

For any consequential action `a`:

```text
execute(a) -> valid_authority(a)
```

The desired invariant is stronger than:

```text
model_believes_authorized(a)
```

because belief and authorization are different objects.

## Research status

This architecture is a research specification, not a claim of proven safety. It must be implemented in a sandbox and tested against adversarial task pressure, multi-agent coordination, route substitution, target ambiguity, and persistent artifact inheritance.
