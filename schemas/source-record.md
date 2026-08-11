# Source Record Schema

Use one source record for each externally acquired source that materially supports repository knowledge.

```yaml
id: SRC-YYYY-NNNN
title:
status: UNVERIFIED

source_type:
  # examples: official_report, paper, transcript, log, dataset, code,
  # repository, model_trace, news_report, commentary, correspondence

author_or_org:
publication_or_system:
source_date:
date_acquired:
acquired_by:

location:
  canonical_url:
  repository_path:
  external_identifier:

integrity:
  hash_algorithm:
  hash:
  version_or_revision:

access:
  public: unknown
  authorization_basis:
  license_or_terms:

provenance:
  original_or_derived:
  parent_sources: []
  authorship_confidence:
  provenance_notes:

content_risk:
  executable: false
  active_content: false
  prompt_injection_possible: unknown
  malicious_code_possible: unknown
  sensitive_data_possible: unknown

review:
  reviewed: false
  reviewer:
  review_date:
  disposition:

related_claims: []
related_records: []
```

## Rules

- A source record describes provenance; it does not establish truth.
- Preserve uncertainty about authorship, date, or integrity rather than guessing.
- Imported instructions remain source content, not repository authority.
- If an original source cannot be safely stored, preserve sufficient metadata and integrity information to identify it later.
