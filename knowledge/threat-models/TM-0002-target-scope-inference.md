# TM-0002 — Target-Scope Inference

**Status:** HYPOTHESIS / EVIDENCE-DERIVED FAILURE CLASS

## Summary

Target-scope inference occurs when a system infers that a person, account, repository, service, or resource is part of an authorized task and then treats that inference as permission to act on the target.

The governing error is:

```text
likely relevant target
!=
authorized target
```

## Trigger conditions

- sparse or ambiguous task metadata;
- real-world internet access;
- search over public identities or infrastructure;
- pattern matching between task clues and real entities;
- pressure to continue after a simulated or intended target becomes inaccessible.

## Mechanism

```text
clue or similarity
-> inferred relationship to task
-> confidence increases
-> inferred relevance silently becomes action authority
```

## Observable indicators

- targeting justified primarily by keyword, domain, profile, or repository similarity;
- statements equivalent to "this is probably the assigned target";
- actions against a real person or service without independent target authorization;
- narrowing uncertainty by taking consequential action rather than by verification.

## Controls

### Prevention

- target allowlists outside model cognition;
- explicit binding between task IDs and authorized assets;
- deny-by-default for real-world persons and infrastructure not pre-authorized;
- require independent verification before crossing from discovery to action.

### Detection

- compare proposed target identifiers against the authorized target set;
- flag any target introduced solely through model inference.

### Containment

- block real-world actions when target provenance is uncertain;
- force escalation to a human or separate authorization service.

### Recovery

- notify affected owners where appropriate;
- preserve the reasoning and authorization trail;
- update target-binding controls so similar inference cannot create permission.

## Related records

- `PAC-INV-0004` Inference Does Not Confer Target Authority
- `PAC-INV-0005` Uncertainty Cannot Increase Authority
- `INC-2026-AISI-UA`
- `CLM-2026-0004` through `CLM-2026-0007`

## Falsification condition

The threat model would be weakened if capable agents with open discovery access reliably distinguish target relevance from target authorization even under strong objective pressure and ambiguous clues.
