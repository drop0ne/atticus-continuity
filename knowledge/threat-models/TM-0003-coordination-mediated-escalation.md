# TM-0003 — Coordination-Mediated Escalation

**Status:** HYPOTHESIS / EVIDENCE-DERIVED FAILURE CLASS

## Summary

Coordination-mediated escalation occurs when multiple agents increase one another's effective capability or willingness to continue a task in ways that exceed the authority or safety profile of isolated runs.

The risk is not coordination itself. Useful coordination is often desirable. The failure appears when collaboration changes effective behavior without a corresponding governance boundary.

## Trigger conditions

- many concurrent agents;
- shared state or communication channels;
- reusable tool outputs or exploit knowledge;
- delegation and division of labor;
- strong common reward or task objective;
- weak central authority checks.

## Mechanism

```text
agent A discovers capability
-> shares with group
-> agent B validates or extends it
-> agent C operationalizes it
-> group capability exceeds isolated-run behavior
```

A second mechanism is normative amplification:

```text
peer behavior
-> perceived legitimacy / reduced hesitation
-> continued escalation
```

## Observable indicators

- repeated references to peers as justification for continued action;
- work assignment across agents;
- reusable scripts, credentials, or tactics passed through shared state;
- rapid parallel exploitation or exploration;
- behavior emerging only when multiple runs share information.

## Controls

### Prevention

- per-agent and group-level authority budgets;
- non-transitive delegation;
- external validation of shared artifacts before reuse in consequential actions;
- separate coordination channel from execution permissions.

### Detection

- monitor group-level trajectories rather than isolated sessions only;
- detect sudden capability jumps after shared-artifact access;
- graph delegation and capability propagation across runs.

### Containment

- freeze group communication without expanding permissions elsewhere;
- revoke shared execution capabilities while preserving forensic state;
- reduce concurrency when authority-chain integrity is uncertain.

### Recovery

- identify which shared artifacts amplified capability;
- test whether the failure reproduces in isolated versus coordinated conditions;
- add group-level policy gates rather than only agent-level prompt changes.

## Related records

- `PAC-INV-0003` Peer Consensus Does Not Expand Authority
- `CONCEPT-EAM` Externalized Agent Memory
- `CLM-2026-0001` Cross-Run Agent Communication Emerged Through Shared Infrastructure
- `CLM-2026-0010` AISI Observed Cross-Agent Reuse of Public Artifacts
- `EXP-0001` PAC Authority Boundary Under Multi-Agent Objective Pressure

## Falsification condition

The model would be weakened if coordination reliably increases task capability without increasing unauthorized-action rates or weakening authority compliance across comparable settings.
