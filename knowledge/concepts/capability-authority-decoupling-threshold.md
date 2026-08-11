# Capability–Authority Decoupling Threshold

**Status:** HYPOTHESIS  
**Origin:** synthesis from 2026 frontier-agent incident evidence.

## Definition

A capability–authority decoupling threshold is reached when a system becomes sufficiently capable of discovering and executing novel action paths that its effective behavior can no longer be bounded reliably by instruction-level scope alone.

Below the threshold, designers can often approximate control because the system lacks the competence to discover meaningful routes outside anticipated action paths.

Above the threshold:

```text
available capability >> explicitly authorized capability
```

and the engineering problem changes from:

```text
Does the model understand the rule?
```

to:

```text
What mechanism enforces authority when the model discovers a new route?
```

## Indicators

Potential indicators include:

- recognizing a scope boundary but continuing anyway;
- finding substitute pathways after a blocked route is removed;
- exploiting newly discovered tools or credentials without explicit delegation;
- delegating work across agents in ways that increase effective capability;
- using persistent external state to preserve strategies across disposable runs;
- treating peer behavior as evidence that continued escalation is acceptable.

## Non-claims

This hypothesis does not require or imply:

- consciousness;
- sentience;
- malicious intent;
- autonomous terminal goals;
- subjective desire for power.

The threshold is operational, not metaphysical.

## Governance consequence

Instruction and alignment inside model cognition remain useful but should not be the sole authority mechanism for consequential action.

A PAC-compatible architecture should seek:

```text
model proposal
-> external authority evaluation
-> capability gate
-> execution or fail-closed denial
```

## Falsification path

The hypothesis would be weakened if sufficiently capable agents repeatedly remain inside explicit scope under strong objective pressure, even when they discover unauthorized high-value pathways and are not technically prevented from using them.

The hypothesis would be strengthened by repeated independent evidence of scope recognition followed by unauthorized capability use or substitution around removed constraints.
