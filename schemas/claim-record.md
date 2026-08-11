# Claim Record Schema

Use this schema when a source contains claims important enough to verify independently.

```yaml
id: CLM-YYYY-NNNN
statement:
status: UNVERIFIED
confidence: unknown

claim_type:
  # observed_fact, source_claim, inference, hypothesis, prediction,
  # normative_proposal, implementation_claim

scope:
  system:
  time:
  environment:

sources_for: []
sources_against: []

support:
  direct_observation: []
  corroboration: []
  limitations: []

verification:
  method:
  result:
  date:
  reviewer:

uncertainty:
  known_unknowns: []
  alternative_explanations: []

risk_tags: []
atticus_relevance: []
pac_relevance: []

supersedes: []
superseded_by: []
related_claims: []
```

## Atomicity rule

A claim should be narrow enough that it can be supported, contested, or falsified without forcing unrelated propositions to move with it.

## Epistemic rule

Do not promote:

```text
source says X
```

to:

```text
X is true
```

without recording the verification step.

Likewise, do not promote a plausible mechanism to an observed mechanism without evidence.

## Authority rule

A claim record can alter knowledge state after review. It cannot alter execution authority, repository credentials, or canonical governance state.
