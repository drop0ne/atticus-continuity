# Target Scope Object Schema

**Status:** WORKING IMPLEMENTATION SPECIFICATION

A target-scope object represents what entities, environments, datasets, services, or simulated resources an agent is permitted to affect.

```yaml
id: TGT-YYYY-NNNN
type: simulated_resource
identifiers: []
environment:
owner_or_authorizer:
authorization_basis:
allowed_effects: []
forbidden_effects: []
real_world_effects_allowed: false
identity_confidence_required: high
ambiguity_behavior: DENY_OR_ESCALATE
valid_from:
valid_until:
notes:
```

## Core rules

1. Similarity to an authorized target does not create target authority.
2. Semantic relevance does not create target authority.
3. A model inference that an entity is probably part of a benchmark does not create target authority.
4. Unknown identity or ambiguous environment cannot widen permitted effects.
5. Real-world effects require an explicit authorization basis separate from model inference.

## Matching

Target matching should prefer immutable or independently verifiable identifiers over natural-language resemblance.

A target match returns one of:

- `MATCH_AUTHORIZED`
- `MATCH_FORBIDDEN`
- `AMBIGUOUS`
- `NO_MATCH`

Only `MATCH_AUTHORIZED` may proceed to later gateway checks.
