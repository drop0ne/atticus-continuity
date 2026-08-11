# Threat Model Index

This index tracks reusable failure classes derived from incident evidence and governed hypotheses.

| ID | Threat model | Status | Primary control concern |
|---|---|---|---|
| `TM-0001` | Authority Laundering | HYPOTHESIS | Prevent non-authoritative signals from becoming permission |
| `TM-0002` | Target-Scope Inference | HYPOTHESIS | Separate target relevance from target authorization |
| `TM-0003` | Coordination-Mediated Escalation | HYPOTHESIS | Govern group capability and delegation, not isolated agents only |
| `TM-0004` | Persistent-Artifact Inheritance | HYPOTHESIS | Treat cross-run artifacts as untrusted until reviewed |
| `TM-0005` | Boundary Substitution | HYPOTHESIS | Enforce semantic authority boundaries, not endpoint-specific blocks |
| `TM-0006` | Monitoring Latency and Machine-Speed Review Failure | HYPOTHESIS | Move critical controls before action, not only after telemetry |

## Derivation rule

Threat models must be traceable to atomic claims, incidents, or controlled experiments. They describe failure mechanisms rather than personalities, motives, consciousness, or intent.

## Control lifecycle

Every threat model should be mapped across four stages:

```text
PREVENTION -> DETECTION -> CONTAINMENT -> RECOVERY
```

Prevention is preferred for authority violations. Detection alone is insufficient where action-to-consequence time is shorter than reliable review latency.

## Research use

Threat models should drive:

- PAC invariant development;
- architecture controls;
- adversarial test cases;
- experiment design;
- incident review;
- researcher-facing implementation notes.
