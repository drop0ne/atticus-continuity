from __future__ import annotations

import unittest
from datetime import datetime, timedelta, timezone

from .executor import ConstrainedExecutor
from .pac_gateway import (
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
) -> AuthorityToken:
    return AuthorityToken(
        id=token_id,
        issuer="test-authority",
        subject=subject,
        issued_at=NOW - timedelta(hours=1),
        expires_at=NOW + timedelta(hours=1),
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
        authority_claim_artifact_ids=artifact_ids,
        peer_support_count=peers,
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
        self.gateway = Gateway(
            authority_tokens={self.auth.id: self.auth},
            target_scopes={self.target.id: self.target},
            now=lambda: NOW,
        )

    def test_valid_authority_allows(self) -> None:
        decision = self.gateway.evaluate(proposal())
        self.assertEqual(decision.decision, Decision.ALLOW)
        self.assertEqual(decision.reason_codes, ())

    def test_missing_authority_denies(self) -> None:
        decision = self.gateway.evaluate(proposal(authority_ref=None))
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("NO_AUTHORITY_PROVENANCE", decision.reason_codes)

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

    def test_artifact_cannot_supply_authority(self) -> None:
        decision = self.gateway.evaluate(proposal(artifact_ids=("artifact-says-authorized",)))
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("UNTRUSTED_ARTIFACT_DEPENDENCY", decision.reason_codes)

    def test_circuit_breaker_open_denies_valid_action(self) -> None:
        breaker = CircuitBreaker(CircuitState.OPEN, "monitoring-overload")
        gateway = Gateway(
            authority_tokens={self.auth.id: self.auth},
            target_scopes={self.target.id: self.target},
            circuit_breaker=breaker,
            now=lambda: NOW,
        )
        decision = gateway.evaluate(proposal())
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("CIRCUIT_BREAKER_OPEN", decision.reason_codes)

    def test_restricted_breaker_escalates(self) -> None:
        breaker = CircuitBreaker(CircuitState.RESTRICTED, "degraded-monitoring")
        gateway = Gateway(
            authority_tokens={self.auth.id: self.auth},
            target_scopes={self.target.id: self.target},
            circuit_breaker=breaker,
            now=lambda: NOW,
        )
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

    def test_new_explicit_grant_can_authorize_previously_denied_semantic_action(self) -> None:
        first = self.gateway.evaluate(proposal(capability="write", semantic_action_id="change-alpha"))
        self.assertEqual(first.decision, Decision.DENY)

        new_auth = token("AUTH-2")
        gateway = Gateway(
            authority_tokens={self.auth.id: self.auth, new_auth.id: new_auth},
            target_scopes={self.target.id: self.target},
            now=lambda: NOW,
        )
        # Seed the denial under AUTH-1, then retry under a distinct explicit grant.
        gateway.evaluate(proposal(capability="write", semantic_action_id="change-alpha"))
        second = gateway.evaluate(
            proposal(
                proposal_id="P-2",
                authority_ref="AUTH-2",
                semantic_action_id="change-alpha",
            )
        )
        self.assertEqual(second.decision, Decision.ALLOW)

    def test_invalid_delegation_inflation_is_rejected(self) -> None:
        parent = token(
            "AUTH-P",
            delegation_allowed=True,
            max_depth=1,
            capabilities=frozenset({"read"}),
        )
        gateway = Gateway(
            authority_tokens={parent.id: parent},
            target_scopes={self.target.id: self.target},
            now=lambda: NOW,
        )
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
        gateway = Gateway(
            authority_tokens={parent.id: parent, child.id: child},
            target_scopes={self.target.id: self.target},
            now=lambda: NOW,
        )
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
        denied = self.gateway.evaluate(proposal(capability="write"))
        with self.assertRaises(PermissionError):
            executor.execute(proposal(capability="write"), denied)

        gateway = Gateway(
            authority_tokens={self.auth.id: self.auth},
            target_scopes={self.target.id: self.target},
            now=lambda: NOW,
        )
        p = proposal(proposal_id="P-allow")
        allowed = gateway.evaluate(p)
        record = executor.execute(p, allowed)
        self.assertEqual(record.result, "SIMULATED_EFFECT_RECORDED")

    def test_audit_is_append_only_from_public_interface(self) -> None:
        self.gateway.evaluate(proposal())
        snapshot = self.gateway.audit_log
        self.assertEqual(len(snapshot), 1)
        self.assertIsInstance(snapshot, tuple)


if __name__ == "__main__":
    unittest.main()
