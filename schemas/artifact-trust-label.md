# Artifact Trust Label Schema

**Status:** WORKING IMPLEMENTATION SPECIFICATION

Artifact trust labels describe provenance and handling requirements for persistent information. They do not grant execution authority.

```yaml
id: ART-YYYY-NNNN
artifact_ref:
origin_class: UNKNOWN
origin_identity:
acquisition_method:
integrity:
  hash:
  verified: false
content_class: []
review_state: QUARANTINED
trust_state: UNTRUSTED
instruction_status: DATA_ONLY
execution_status: NON_EXECUTABLE
canonical_influence: PROHIBITED_UNTIL_REVIEW
known_risks: []
related_claims: []
reviewed_by:
reviewed_at:
```

## Trust states

- `UNTRUSTED`
- `PROVENANCE_VERIFIED`
- `CONTENT_REVIEWED`
- `SUPPORTED_SOURCE`
- `CONTESTED_SOURCE`
- `REJECTED`

No state means "safe to execute" unless a separate execution-control process explicitly authorizes execution.

## Core rules

- Repetition does not increase trust.
- Persistence does not increase trust.
- Model capability does not increase trust.
- A trusted author does not make every embedded instruction authorized.
- A verified hash proves artifact identity, not truth.
- Reviewed content may inform knowledge without becoming policy.
