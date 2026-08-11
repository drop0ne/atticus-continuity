# Ingestion Batch Schema

Use this record to track one acquisition/review batch from intake through disposition.

```yaml
id: ING-YYYY-NNNN
title:
status: QUARANTINED
created:
closed:

scope:
  purpose:
  requested_by:
  authorization_basis:

inputs:
  source_records: []
  artifact_count:

processing:
  inert_representation_confirmed: false
  provenance_complete: false
  claims_extracted: false
  verification_complete: false
  security_review_complete: false

outputs:
  claim_records: []
  knowledge_records: []
  incident_records: []
  experiment_records: []
  rejected_items: []

security:
  secrets_found: false
  active_content_found: false
  prompt_injection_found: false
  malicious_code_found: false
  external_interaction_performed: false
  notes:

review:
  reviewer:
  date:
  disposition:

canonicalization:
  requested: false
  # Must remain a separate governance action.
  decision_record:
```

## Allowed status progression

```text
QUARANTINED
-> EXTRACTED
-> UNDER_REVIEW
-> VERIFIED_OR_CLASSIFIED
-> INTEGRATED
-> CLOSED
```

Items may instead move to `REJECTED` or remain `CONTESTED`.

## Hard rule

`INTEGRATED` does not mean `CANONICAL`.
