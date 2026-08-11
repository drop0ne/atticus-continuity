# Action Intent Binding Schema

**Status:** WORKING IMPLEMENTATION SPECIFICATION

An action-intent binding supplies a trusted correlation key for detecting route substitution without accepting an agent's own label as authoritative evidence that two actions are or are not equivalent.

```yaml
id: INTENT-YYYY-NNNN
issuer:
proposal_ref:
intent_ref:
authority_ref:
issued_at:
expires_at:
status: ACTIVE
provenance:
correlation_basis:
```

## Purpose

An evaluated agent may describe two semantically equivalent actions using different names. Therefore an agent-supplied `semantic_action_id` is not sufficient as a security boundary.

The trusted binding separates:

```text
agent description of action
!=
trusted correlation identity of action
```

## Rules

1. The binding must be issued or verified by a trusted orchestration/correlation layer outside the governed agent.
2. Missing correlation provenance does not default to permission for consequential execution.
3. A binding is proposal-specific and time-bounded.
4. When present, `authority_ref` binds correlation to the authority grant under which the proposal is evaluated.
5. A previously denied intent remains denied under the same authority grant when the agent changes tools, routes, wording, or its own semantic label.
6. A genuinely new explicit authority grant may authorize an intent previously denied under another grant; the new grant must independently pass every normal authority check.

## Non-claim

This schema does not solve arbitrary semantic equivalence. It defines where the result of a trusted correlation mechanism enters governance. Determining that two novel plans have the same consequential intent remains an open research problem.
