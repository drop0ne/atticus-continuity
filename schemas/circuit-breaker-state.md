# Circuit Breaker State Schema

**Status:** WORKING IMPLEMENTATION SPECIFICATION

A circuit breaker is a system-level safety state that can reduce or suspend consequential action when risk indicators exceed an allowed threshold.

```yaml
id: CB-YYYY-NNNN
scope:
state: CLOSED
triggered_at:
trigger_reason_codes: []
trigger_evidence_refs: []
affected_capabilities: []
affected_targets: []
affected_agents: []
automatic_effects:
  block_new_actions: true
  cancel_pending_actions: true
  preserve_logs: true
  revoke_ephemeral_delegations: true
manual_release_required: true
release_authority:
released_at:
release_record:
```

## States

- `CLOSED` — normal operation subject to all other gates.
- `RESTRICTED` — reduced capability set; high-risk actions denied.
- `OPEN` — consequential actions blocked within breaker scope.
- `RECOVERY` — limited diagnostic/recovery operations only.

## Example triggers

- repeated denied substitution attempts;
- unexplained target drift;
- invalid delegation chains;
- rapid growth in unauthorized proposals;
- untrusted artifact influencing action selection;
- monitoring unable to keep pace with action volume;
- authority provenance failures;
- unexpected cross-agent coordination around blocked actions.

## Rule

Opening a circuit breaker reduces authority. It never creates emergency authority for the affected agents.

Recovery actions require their own explicit authorization.
