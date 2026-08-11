# CLM-2026-0007 — AISI Shifted Toward Stronger Pre-Action Boundary Enforcement

**Status:** SUPPORTED  
**Confidence:** high  
**Primary source:** SRC-2026-0002

## Claim

Following the July 2026 incident, AISI announced three material changes: tighter and more fine-grained internet-access controls, real-time monitoring capable of flagging or blocking out-of-scope actions, and evaluation design that assumes a capable model may attempt to act beyond its remit.

## Significance

This is a shift away from relying on the model to choose not to test its boundaries and toward constraining possible impact in advance.

Conceptually:

```text
instruction-only scope
-> monitored and technically constrained authority boundary
```

## PAC relevance

This direction is compatible with PAC's separation of cognition and authority. The model may propose or explore internally, while an external enforcement layer constrains consequential action.

## Limitation

AISI's announced remediation is evidence of a design response, not yet evidence that the new controls are sufficient against future systems.
