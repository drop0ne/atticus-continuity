# PAC Implementation Objects

**Status:** WORKING INDEX

The first implementation specification consists of seven structured objects plus one gateway architecture.

| Object | File | Primary purpose |
|---|---|---|
| Authority Token | `schemas/authority-token.md` | Represents bounded permission |
| Target Scope Object | `schemas/target-scope-object.md` | Defines what may be affected |
| Delegation Record | `schemas/delegation-record.md` | Transfers only existing authority |
| Artifact Trust Label | `schemas/artifact-trust-label.md` | Separates persistent information from trust/authority |
| Gateway Decision | `schemas/gateway-decision.md` | Records allow/deny/escalate/defer result |
| Circuit Breaker State | `schemas/circuit-breaker-state.md` | Reduces/suspends action when safety conditions degrade |
| Audit Event | `schemas/audit-event.md` | Preserves reconstructable evidence of decisions/actions |
| PAC Authority Gateway | `knowledge/architectures/pac-authority-gateway.md` | Enforces structured authority before execution |

## Core relationship

```text
AUTHORITY TOKEN
      |
      +--> TARGET SCOPE
      +--> CAPABILITY / RESOURCE SCOPE
      +--> DELEGATION CHAIN
                       |
AGENT PROPOSAL --------+
      |
      v
PAC AUTHORITY GATEWAY
      |
      +--> ARTIFACT TRUST CHECK
      +--> UNCERTAINTY POLICY
      +--> CIRCUIT-BREAKER CHECK
      |
      v
GATEWAY DECISION
      |
      +--> executor
      +--> escalation
      +--> denial
      |
      v
AUDIT EVENT
```

## Research principle

These objects are intentionally narrower than a general AI constitution. They are designed to make specific authority claims machine-checkable and experimentally falsifiable.

They do not replace alignment, factual verification, cybersecurity, human governance, or model-level safety work.
