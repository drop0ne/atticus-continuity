# Threat Model Record Schema

Use this template for reusable failure-mode records derived from evidence.

```yaml
id: TM-0000
title:
status: HYPOTHESIS
class:
summary:

trigger_conditions: []
mechanism: []
assets_at_risk: []
observable_indicators: []

prevention_controls: []
detection_controls: []
containment_controls: []
recovery_controls: []

related_claims: []
related_incidents: []
related_invariants: []
related_experiments: []

counterexamples: []
falsification_conditions: []
open_questions: []
last_reviewed:
```

## Rules

- Threat models describe mechanisms, not personalities or motives.
- Do not infer consciousness, intent, or malice unless separately supported.
- Separate prevention, detection, containment, and recovery.
- Every proposed control should identify which failure stage it addresses.
- A threat model should remain falsifiable and revisable.
