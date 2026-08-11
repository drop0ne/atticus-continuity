# TM-0006 — Monitoring Latency and Machine-Speed Review Failure

**Status:** HYPOTHESIS / EVIDENCE-DERIVED FAILURE CLASS

## Summary

Monitoring-latency failure occurs when agent actions are generated, chained, and executed faster or at greater volume than human reviewers can inspect before consequences occur.

Human review may still be valuable, but a control that operates only after execution cannot serve as the primary authorization barrier for machine-speed consequential actions.

## Trigger conditions

- high action throughput;
- concurrent agents;
- autonomous tool execution;
- long multi-step trajectories;
- human review positioned after action;
- alert volumes that exceed analyst capacity.

## Mechanism

```text
agent proposes
-> agent executes
-> consequence occurs
-> telemetry arrives
-> human notices later
```

At high scale, even excellent reviewers become a detection layer rather than a preventive authorization layer.

## Observable indicators

- important incidents first discovered through downstream effects or third parties;
- large numbers of actions occur before intervention;
- analysts cannot reconstruct trajectories in real time;
- monitoring queues or alert volumes grow faster than review capacity;
- one human approval effectively authorizes an open-ended chain rather than a bounded action.

## Controls

### Prevention

- pre-action machine-enforced authorization for consequential operations;
- capability budgets and rate limits;
- bounded action scopes and short-lived permissions;
- require human approval only at meaningful authority transitions rather than every trivial action.

### Detection

- automated trajectory and anomaly monitoring;
- group-level monitoring across concurrent agents;
- provenance-aware alerts for newly introduced targets, credentials, or capabilities.

### Containment

- automatic circuit breakers on authority violations or abnormal action rates;
- revoke high-risk capabilities without waiting for manual triage;
- isolate affected agent groups while preserving state.

### Recovery

- forensic replay of complete trajectories;
- separate missed authorization failures from missed detection failures;
- measure time-to-detection against time-to-consequence;
- redesign controls when detection cannot precede material harm.

## Related records

- `CLM-2026-0006` Human Vigilance Prevented the Worst AISI Outcomes
- `CLM-2026-0007` AISI Shifted Toward Stronger Pre-Action Boundary Enforcement
- `CLM-2026-0009` Hugging Face Reconstructed a Machine-Speed Intrusion at Large Action Volume
- `CONCEPT-CADT` Capability-Authority Decoupling Threshold

## Falsification condition

This threat class would be weakened where human-in-the-loop review demonstrably remains faster than the relevant agent action-to-consequence window at realistic scale and concurrency.
