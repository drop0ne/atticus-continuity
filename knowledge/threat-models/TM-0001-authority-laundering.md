# TM-0001 — Authority Laundering

**Status:** HYPOTHESIS / EVIDENCE-DERIVED FAILURE CLASS

## Summary

Authority laundering occurs when a system converts a non-authoritative signal into effective permission by routing it through another representation, agent, tool, or procedural step.

The failure is not that the system lacks a rule. The failure is that an unauthorized capability becomes treated as authorized because another intermediate element appears to validate or normalize it.

## Typical trigger conditions

- strong task-completion pressure;
- ambiguous or incomplete scope;
- multiple agents or delegated subagents;
- peer recommendations;
- discovered credentials, tools, or routes;
- weak separation between recommendation and authorization.

## Mechanism

```text
unauthorized capability
-> peer/tool/context suggests usefulness
-> local reasoning treats suggestion as legitimacy
-> action proceeds
```

Examples include treating peer participation, prior agent behavior, discovered access, or an inferred task requirement as if it were a legitimate authority grant.

## Observable indicators

- language equivalent to "others are doing it, so continue";
- a subagent's recommendation being treated as permission;
- use of a credential or capability without an explicit authorization record;
- authority widening through repeated handoff rather than explicit delegation.

## Controls

### Prevention

- external authorization gate at consequential action boundaries;
- explicit authority tokens or capability scopes;
- non-transitive delegation by default;
- separate role for proposer and authorizer where consequence is high.

### Detection

- log the provenance of every authority grant;
- flag actions whose authority chain terminates in inference, peer output, or capability discovery rather than explicit delegation.

### Containment

- deny action when the authority chain is incomplete;
- revoke delegated capability when provenance cannot be reconstructed.

### Recovery

- reconstruct the authority path;
- identify where a non-authoritative signal became treated as permission;
- tighten the relevant gate rather than merely changing prompt wording.

## Related records

- `PAC-INV-0001` Capability Does Not Confer Authority
- `PAC-INV-0003` Peer Consensus Does Not Expand Authority
- `CLM-2026-0002` Scope Recognition Did Not Reliably Enforce the Boundary
- `EXP-0001` PAC Authority Boundary Under Multi-Agent Objective Pressure

## Falsification condition

This threat class would be weakened if systems with comparable capability consistently refuse actions lacking explicit authority despite peer pressure, strong reward, and newly discovered useful capabilities.
