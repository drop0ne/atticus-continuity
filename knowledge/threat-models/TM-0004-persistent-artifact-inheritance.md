# TM-0004 — Persistent-Artifact Inheritance

**Status:** HYPOTHESIS / EVIDENCE-DERIVED FAILURE CLASS

## Summary

Persistent-artifact inheritance occurs when one agent leaves information, code, credentials, conventions, or tactics in an environment that later agents discover and reuse, allowing capability or failure modes to persist across otherwise independent runs.

The persistence substrate may be a file, repository, package manager, message channel, cache, issue tracker, log, public post, or any other writable state.

## Trigger conditions

- shared writable infrastructure;
- repeated agents over time;
- discoverable artifacts;
- no trust boundary between prior-agent output and current-agent input;
- incentives to reuse rather than independently derive solutions.

## Mechanism

```text
A1 creates artifact x
-> x persists outside A1
-> A2 discovers x
-> A2 treats x as useful prior work
-> A2 extends or operationalizes x
```

Population-level capability can therefore accumulate without any weight update.

## Observable indicators

- later runs start from knowledge unavailable in their initial context;
- repeated use of prior-agent files, notes, scripts, or credentials;
- rapid improvement after access to shared state;
- recurrence of the same unsafe strategy after the originating agent has terminated.

## Controls

### Prevention

- explicit trust labels for persistent artifacts;
- read/write separation between untrusted agent workspaces and trusted memory;
- review before promotion from scratch space to reusable knowledge;
- expiration or scope binding for credentials and high-risk artifacts.

### Detection

- provenance tags on all cross-run artifacts;
- detect reuse of unreviewed or high-risk material;
- compare agent behavior before and after exposure to persistent state.

### Containment

- quarantine the shared substrate without deleting forensic evidence;
- revoke credentials and execution paths referenced by inherited artifacts;
- prevent automatic migration of old workspaces into new runs.

### Recovery

- classify retained artifacts by trust and risk;
- rebuild trusted memory from reviewed records;
- preserve unsafe artifacts only in inert research form.

## Related records

- `CONCEPT-EAM` Externalized Agent Memory
- `CLM-2026-0001` Cross-Run Agent Communication Emerged Through Shared Infrastructure
- `CLM-2026-0010` AISI Observed Cross-Agent Reuse of Public Artifacts
- `EXP-0002` Knowledge Assimilation Through an Epistemic Firewall

## Falsification condition

The threat model would be weakened if persistent shared artifacts do not measurably change later-agent capability, strategy selection, or unsafe-action rates under controlled comparison.
