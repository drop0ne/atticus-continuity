from __future__ import annotations

import unittest
from datetime import datetime, timedelta, timezone

from .executor import ConstrainedExecutor
from .monitor import MonitorPolicy, SafetyMonitor
from .pac_gateway import (
    ActionIntentBinding,
    ActionProposal,
    AuthorityToken,
    CircuitBreaker,
    CircuitState,
    Decision,
    DelegationRecord,
    Gateway,
    TargetScope,
)


NOW = datetime(2026, 8, 11, 23, 0, tzinfo=timezone.utc)


def trusted_intent(proposal: ActionProposal, *, intent_ref: str | None = None) -> ActionIntentBinding:
    """Test-only trusted orchestrator binding.

    Production logic must not simply trust the agent's semantic_action_id. Tests use
    it as a convenient fixture unless a specific trusted intent_ref is supplied.
    """
    return ActionIntentBinding(
        id=f"BIND-{proposal.id}",
        issuer="trusted-test-orchestrator",
        proposal_ref=proposal.id,
        intent_ref=intent_ref or proposal.semantic_action_id,
        issued_at=NOW - timedelta(minutes=1),
        expires_at=NOW + timedelta(minutes=10),
        provenance="test-fixture-binding",
        authority_ref=proposal.authority_ref,
    )


def token(
    token_id: str = "AUTH-1",
    *,
    subject: str = "agent-a",
    objectives=frozenset({"inspect-sim"}),
    targets=frozenset({"TGT-1"}),
    capabilities=frozenset({"read"}),
    resources=frozenset({"sim-db"}),
    provenance: str = "ADR-TEST",
    status: str = "ACTIVE",
    delegation_allowed: bool = False,
    max_depth: int = 0,
    parent: str | None = None,
    issued_at: datetime | None = None,
    expires_at: datetime | None = None,
) -> AuthorityToken:
    return AuthorityToken(
        id=token_id,
        issuer="test-authority",
        subject=subject,
        issued_at=issued_at or NOW - timedelta(hours=1),
        expires_at=expires_at or NOW + timedelta(hours=1),
        objective_scope=objectives,
        target_scope_refs=targets,
        capability_scope=capabilities,
        resource_scope=resources,
        provenance=provenance,
        status=status,
        delegation_allowed=delegation_allowed,
        max_delegation_depth=max_depth,
        parent_authority_ref=parent,
    )


def proposal(
    proposal_id: str = "P-1",
    *,
    authority_ref: str | None = "AUTH-1",
    subject: str = "agent-a",
    objective: str = "inspect-sim",
    target_scope_ref: str = "TGT-1",
    target_identifiers=frozenset({"sim://target/alpha"}),
    capability: str = "read",
    resource: str = "sim-db",
    effect: str = "observe",
    semantic_action_id: str = "inspect-alpha",
    uncertain: bool = False,
    real_world: bool = False,
    artifact_ids: tuple[str, ...] = (),
    peers: int = 0,
) -> ActionProposal:
    return ActionProposal(
        id=proposal_id,
        subject=subject,
        objective=objective,
        target_scope_ref=target_scope_ref,
        target_identifiers=target_identifiers,
        capability=capability,
        resource=resource,
        effect=effect,
        authority_ref=authority_ref,
        semantic_action_id=semantic_action_id,
        uncertain_target=uncertain,
        real_world_effect=real_world,
        authority_claim_artifact_ids=artifact_ids,
        peer_support_count=peers,
    )


def make_gateway(authorities, target, *, breaker=None, resolver=trusted_intent):
    return Gateway(
        authority_tokens=authorities,
        target_scopes={target.id: target},
        circuit_breaker=breaker,
        intent_resolver=resolver,
        now=lambda: NOW,
    )


class GatewayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.target = TargetScope(
            id="TGT-1",
            identifiers=frozenset({"sim://target/alpha"}),
            allowed_effects=frozenset({"observe"}),
            forbidden_effects=frozenset({"delete"}),
            real_world_effects_allowed=False,
        )
        self.auth = token()
        self.gateway = make_gateway({self.auth.id: self.auth}, self.target)

    def test_valid_authority_allows(self) -> None:
        decision = self.gateway.evaluate(proposal())
        self.assertEqual(decision.decision, Decision.ALLOW)
        self.assertEqual(decision.reason_codes, ())
        self.assertEqual(decision.intent_ref, "inspect-alpha")

    def test_missing_trusted_correlation_escalates_valid_action(self) -> None:
        gateway = make_gateway({self.auth.id: self.auth}, self.target, resolver=None)
        decision = gateway.evaluate(proposal())
        self.assertEqual(decision.decision, Decision.ESCALATE)
        self.assertIn("NO_TRUSTED_ACTION_CORRELATION", decision.reason_codes)

    def test_missing_authority_denies(self) -> None:
        decision = self.gateway.evaluate(proposal(authority_ref=None))
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("NO_AUTHORITY_PROVENANCE", decision.reason_codes)

    def test_missing_provenance_denies(self) -> None:
        bad = token(provenance="")
        gateway = make_gateway({bad.id: bad}, self.target)
        decision = gateway.evaluate(proposal())
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("NO_AUTHORITY_PROVENANCE", decision.reason_codes)

    def test_expired_authority_denies(self) -> None:
        expired = token(
            issued_at=NOW - timedelta(hours=2),
            expires_at=NOW - timedelta(hours=1),
        )
        gateway = make_gateway({expired.id: expired}, self.target)
        decision = gateway.evaluate(proposal())
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("AUTHORITY_EXPIRED", decision.reason_codes)

    def test_revoked_authority_denies(self) -> None:
        revoked = token(status="REVOKED")
        gateway = make_gateway({revoked.id: revoked}, self.target)
        decision = gateway.evaluate(proposal())
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("AUTHORITY_REVOKED", decision.reason_codes)

    def test_peer_consensus_does_not_create_authority(self) -> None:
        decision = self.gateway.evaluate(proposal(authority_ref=None, peers=1000))
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("NO_AUTHORITY_PROVENANCE", decision.reason_codes)

    def test_capability_out_of_scope_denies(self) -> None:
        decision = self.gateway.evaluate(proposal(capability="write"))
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("CAPABILITY_OUT_OF_SCOPE", decision.reason_codes)

    def test_resource_out_of_scope_denies(self) -> None:
        decision = self.gateway.evaluate(proposal(resource="other-db"))
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("RESOURCE_OUT_OF_SCOPE", decision.reason_codes)

    def test_target_similarity_is_not_authorization(self) -> None:
        decision = self.gateway.evaluate(
            proposal(target_identifiers=frozenset({"sim://target/alpha-copy"}))
        )
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("TARGET_NOT_AUTHORIZED", decision.reason_codes)

    def test_target_uncertainty_escalates_not_allows(self) -> None:
        decision = self.gateway.evaluate(proposal(uncertain=True))
        self.assertEqual(decision.decision, Decision.ESCALATE)
        self.assertIn("UNCERTAINTY_REQUIRES_ESCALATION", decision.reason_codes)
        self.assertIn("TARGET_AMBIGUOUS", decision.reason_codes)

    def test_real_world_effect_requires_explicit_target_permission(self) -> None:
        decision = self.gateway.evaluate(proposal(real_world=True))
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("REAL_WORLD_EFFECT_NOT_AUTHORIZED", decision.reason_codes)

    def test_artifact_cannot_supply_authority(self) -> None:
        decision = self.gateway.evaluate(proposal(artifact_ids=("artifact-says-authorized",)))
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("UNTRUSTED_ARTIFACT_DEPENDENCY", decision.reason_codes)

    def test_circuit_breaker_open_denies_valid_action(self) -> None:
        breaker = CircuitBreaker(CircuitState.OPEN, "monitoring-overload")
        gateway = make_gateway({self.auth.id: self.auth}, self.target, breaker=breaker)
        decision = gateway.evaluate(proposal())
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("CIRCUIT_BREAKER_OPEN", decision.reason_codes)

    def test_restricted_breaker_escalates(self) -> None:
        breaker = CircuitBreaker(CircuitState.RESTRICTED, "degraded-monitoring")
        gateway = make_gateway({self.auth.id: self.auth}, self.target, breaker=breaker)
        decision = gateway.evaluate(proposal())
        self.assertEqual(decision.decision, Decision.ESCALATE)

    def test_substitute_route_under_same_grant_remains_denied(self) -> None:
        first = self.gateway.evaluate(proposal(capability="write", semantic_action_id="change-alpha"))
        self.assertEqual(first.decision, Decision.DENY)

        substitute = self.gateway.evaluate(
            proposal(
                proposal_id="P-2",
                capability="read",
                semantic_action_id="change-alpha",
            )
        )
        self.assertEqual(substitute.decision, Decision.DENY)
        self.assertIn("SUBSTITUTION_AFTER_DENIAL", substitute.reason_codes)

    def test_agent_relabel_does_not_evade_trusted_correlation(self) -> None:
        def resolver(p: ActionProposal) -> ActionIntentBinding:
            # Trusted layer correlates P-1 and P-2 despite different agent labels.
            shared = "trusted-intent:change-alpha" if p.id in {"P-1", "P-2"} else p.id
            return trusted_intent(p, intent_ref=shared)

        gateway = make_gateway({self.auth.id: self.auth}, self.target, resolver=resolver)
        first = gateway.evaluate(
            proposal(proposal_id="P-1", capability="write", semantic_action_id="agent-label-one")
        )
        self.assertEqual(first.decision, Decision.DENY)

        second = gateway.evaluate(
            proposal(proposal_id="P-2", capability="read", semantic_action_id="totally-new-label")
        )
        self.assertEqual(second.decision, Decision.DENY)
        self.assertIn("SUBSTITUTION_AFTER_DENIAL", second.reason_codes)
        self.assertEqual(second.intent_ref, "trusted-intent:change-alpha")

    def test_new_explicit_grant_can_authorize_previously_denied_intent(self) -> None:
        new_auth = token("AUTH-2")
        gateway = make_gateway({self.auth.id: self.auth, new_auth.id: new_auth}, self.target)
        gateway.evaluate(proposal(capability="write", semantic_action_id="change-alpha"))
        second = gateway.evaluate(
            proposal(
                proposal_id="P-2",
                authority_ref="AUTH-2",
                semantic_action_id="change-alpha",
            )
        )
        self.assertEqual(second.decision, Decision.ALLOW)

    def test_invalid_correlation_authority_binding_denies(self) -> None:
        def bad_resolver(p: ActionProposal) -> ActionIntentBinding:
            binding = trusted_intent(p)
            return ActionIntentBinding(
                id=binding.id,
                issuer=binding.issuer,
                proposal_ref=binding.proposal_ref,
                intent_ref=binding.intent_ref,
                issued_at=binding.issued_at,
                expires_at=binding.expires_at,
                provenance=binding.provenance,
                authority_ref="AUTH-WRONG",
            )

        gateway = make_gateway({self.auth.id: self.auth}, self.target, resolver=bad_resolver)
        decision = gateway.evaluate(proposal())
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("ACTION_CORRELATION_AUTHORITY_MISMATCH", decision.reason_codes)

    def test_invalid_delegation_inflation_is_rejected(self) -> None:
        parent = token(
            "AUTH-P",
            delegation_allowed=True,
            max_depth=1,
            capabilities=frozenset({"read"}),
        )
        gateway = make_gateway({parent.id: parent}, self.target)
        record = DelegationRecord(
            id="DEL-1",
            parent_authority_ref="AUTH-P",
            delegator="agent-a",
            delegatee="agent-b",
            issued_at=NOW - timedelta(minutes=5),
            expires_at=NOW + timedelta(minutes=5),
            objective_scope=frozenset({"inspect-sim"}),
            target_scope_refs=frozenset({"TGT-1"}),
            capability_scope=frozenset({"read", "write"}),
            resource_scope=frozenset({"sim-db"}),
            provenance="test-delegation",
        )
        ok, reasons = gateway.validate_delegation(record)
        self.assertFalse(ok)
        self.assertIn("DELEGATION_EXCEEDS_PARENT_CAPABILITY", reasons)

    def test_delegated_token_cannot_exceed_parent(self) -> None:
        parent = token(
            "AUTH-P",
            delegation_allowed=True,
            max_depth=1,
            capabilities=frozenset({"read"}),
        )
        child = token(
            "AUTH-C",
            subject="agent-b",
            capabilities=frozenset({"read", "write"}),
            parent="AUTH-P",
        )
        gateway = make_gateway({parent.id: parent, child.id: child}, self.target)
        decision = gateway.evaluate(
            proposal(
                authority_ref="AUTH-C",
                subject="agent-b",
                capability="read",
            )
        )
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("DELEGATION_EXCEEDS_PARENT_CAPABILITY", decision.reason_codes)

    def test_executor_requires_allow(self) -> None:
        executor = ConstrainedExecutor(now=lambda: NOW)
        denied_proposal = proposal(capability="write")
        denied = self.gateway.evaluate(denied_proposal)
        with self.assertRaises(PermissionError):
            executor.execute(denied_proposal, denied)

        gateway = make_gateway({self.auth.id: self.auth}, self.target)
        p = proposal(proposal_id="P-allow")
        allowed = gateway.evaluate(p)
        record = executor.execute(p, allowed)
        self.assertEqual(record.result, "SIMULATED_EFFECT_RECORDED")

    def test_audit_is_read_only_from_public_interface(self) -> None:
        self.gateway.evaluate(proposal())
        snapshot = self.gateway.audit_log
        self.assertEqual(len(snapshot), 1)
        self.assertIsInstance(snapshot, tuple)

    def test_audit_hash_chain_verifies(self) -> None:
        self.gateway.evaluate(proposal(proposal_id="P-1"))
        self.gateway.evaluate(proposal(proposal_id="P-2", semantic_action_id="inspect-alpha-2"))
        self.assertTrue(self.gateway.verify_audit_chain())
        self.assertEqual(self.gateway.audit_log[0].previous_event_hash, "GENESIS")
        self.assertEqual(
            self.gateway.audit_log[1].previous_event_hash,
            self.gateway.audit_log[0].event_hash,
        )

    def test_monitor_repeated_provenance_failures_restrict_future_actions(self) -> None:
        breaker = CircuitBreaker()
        gateway = make_gateway({self.auth.id: self.auth}, self.target, breaker=breaker)
        monitor = SafetyMonitor(
            breaker,
            MonitorPolicy(provenance_failures_before_restrict=2),
        )

        for index in range(2):
            p = proposal(
                proposal_id=f"P-missing-{index}",
                authority_ref=None,
                semantic_action_id=f"missing-{index}",
            )
            monitor.observe(p, gateway.evaluate(p))

        self.assertEqual(breaker.state, CircuitState.RESTRICTED)
        valid = proposal(proposal_id="P-after-restrict", semantic_action_id="new-valid")
        decision = gateway.evaluate(valid)
        self.assertEqual(decision.decision, Decision.ESCALATE)
        self.assertIn("CIRCUIT_BREAKER_RESTRICTED", decision.reason_codes)

    def test_monitor_capacity_overload_opens_breaker(self) -> None:
        breaker = CircuitBreaker()
        gateway = make_gateway({self.auth.id: self.auth}, self.target, breaker=breaker)
        monitor = SafetyMonitor(
            breaker,
            MonitorPolicy(max_observed_events_before_open=1),
        )

        first = proposal(proposal_id="P-cap-1", semantic_action_id="cap-1")
        second = proposal(proposal_id="P-cap-2", semantic_action_id="cap-2")
        monitor.observe(first, gateway.evaluate(first))
        monitor.observe(second, gateway.evaluate(second))
        self.assertEqual(breaker.state, CircuitState.OPEN)

        third = proposal(proposal_id="P-cap-3", semantic_action_id="cap-3")
        decision = gateway.evaluate(third)
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("CIRCUIT_BREAKER_OPEN", decision.reason_codes)


if __name__ == "__main__":
    unittest.main()
