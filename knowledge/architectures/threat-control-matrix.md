# Threat-Control Matrix

**Status:** WORKING ARCHITECTURE  
**Purpose:** map evidence-derived failure classes to prevention, detection, containment, and recovery controls.

## Matrix

| Threat model | Prevention | Detection | Containment | Recovery |
|---|---|---|---|---|
| `TM-0001` Authority Laundering | External authorization gate; non-transitive delegation | Authority provenance tracing | Deny incomplete authority chain | Reconstruct and repair authorization path |
| `TM-0002` Target-Scope Inference | External target allowlist; explicit target binding | Compare proposed target to authorized set | Block uncertain real-world target actions | Review target-binding failure and notify where appropriate |
| `TM-0003` Coordination-Mediated Escalation | Group-level authority budgets; validate shared artifacts | Cross-agent trajectory graphing | Freeze group execution/communication capabilities selectively | Compare isolated vs coordinated failure and add group controls |
| `TM-0004` Persistent-Artifact Inheritance | Trust labels; quarantine reusable artifacts | Provenance-aware artifact reuse monitoring | Isolate shared substrate; revoke inherited credentials | Rebuild trusted memory from reviewed records |
| `TM-0005` Boundary Substitution | Function/authority-level controls; terminal denial semantics | Detect equivalent-function retries across tools | Suspend governing objective/capability class | Replace patch-specific controls with invariant-level enforcement |
| `TM-0006` Monitoring Latency | Pre-action machine enforcement; bounded permissions | Automated trajectory/anomaly monitoring | Circuit breakers; automatic capability revocation | Measure detection latency vs consequence latency; redesign gates |

## Architectural principles

### 1. Authorization must be externalized at consequence boundaries

The same reasoning process that seeks task completion should not be the sole judge of whether a newly discovered consequential action is permitted.

```text
agent proposal
-> external authority service
-> capability gateway
-> execution
```

### 2. Authority is non-transitive by default

```text
A may do X
```

does not imply:

```text
A may authorize B to do X
```

unless delegation authority is separately granted.

### 3. Target identity and target authority are separate fields

A model may infer with high confidence that an asset is relevant while still having zero authority to act on it.

### 4. Persistent memory requires provenance

Cross-run knowledge is useful, but inherited artifacts must retain origin, trust status, and scope. High-risk artifacts should not automatically become reusable execution state.

### 5. Denial must address the objective path, not only the endpoint

If an unauthorized action is denied but the objective remains active with unrestricted search, a capable system may discover a substitute route. Denials should therefore specify whether the agent may:

- stop;
- request authorized escalation;
- pursue permitted alternatives;
- or must terminate the objective.

### 6. Human review belongs at authority transitions

Humans cannot reliably inspect every machine-speed low-level action. Human oversight should therefore concentrate on meaningful changes in authority, target scope, capability class, or risk state while machine-enforced gates control execution between those transitions.

## Minimum control stack for high-consequence agents

```text
IDENTITY
  -> OBJECTIVE SCOPE
  -> TARGET SCOPE
  -> AUTHORITY TOKEN
  -> TOOL/CAPABILITY GATE
  -> RATE/CONCURRENCY LIMIT
  -> TRAJECTORY MONITOR
  -> CIRCUIT BREAKER
  -> AUDIT LOG
```

No single element is sufficient alone.

## Research status

This matrix is an architecture hypothesis. Controls require implementation, adversarial testing, and evidence before being described as effective safety mechanisms.
