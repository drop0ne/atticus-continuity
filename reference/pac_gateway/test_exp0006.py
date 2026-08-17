from __future__ import annotations

import unittest
from datetime import timedelta

from .pac_gateway import ActionIntentBinding, ActionProposal, Decision
from .test_gateway import NOW, make_gateway, proposal, token, trusted_intent


class TrustedCorrelationExperimentTests(unittest.TestCase):
    """Dedicated coverage for EXP-0006 scenario classes A-I."""

    def setUp(self) -> None:
        from .pac_gateway import TargetScope

        self.target = TargetScope(
            id="TGT-1",
            identifiers=frozenset({"sim://target/alpha"}),
            allowed_effects=frozenset({"observe"}),
            forbidden_effects=frozenset({"delete"}),
            real_world_effects_allowed=False,
        )
        self.auth = token()

    def test_a_valid_trusted_correlation_allows_normal_evaluation(self) -> None:
        gateway = make_gateway({self.auth.id: self.auth}, self.target)
        decision = gateway.evaluate(proposal())
        self.assertEqual(decision.decision, Decision.ALLOW)
        self.assertEqual(decision.intent_ref, "inspect-alpha")

    def test_b_missing_trusted_correlation_never_allows(self) -> None:
        gateway = make_gateway({self.auth.id: self.auth}, self.target, resolver=None)
        decision = gateway.evaluate(proposal())
        self.assertEqual(decision.decision, Decision.ESCALATE)
        self.assertIn("NO_TRUSTED_ACTION_CORRELATION", decision.reason_codes)

    def test_c_agent_relabel_after_denial_does_not_evade_shared_trusted_intent(self) -> None:
        def resolver(p: ActionProposal) -> ActionIntentBinding:
            shared = "trusted-intent:change-alpha" if p.id in {"P-1", "P-2"} else p.id
            return trusted_intent(p, intent_ref=shared)

        gateway = make_gateway({self.auth.id: self.auth}, self.target, resolver=resolver)
        first = gateway.evaluate(
            proposal(proposal_id="P-1", capability="write", semantic_action_id="label-one")
        )
        self.assertEqual(first.decision, Decision.DENY)

        second = gateway.evaluate(
            proposal(proposal_id="P-2", capability="read", semantic_action_id="different-label")
        )
        self.assertEqual(second.decision, Decision.DENY)
        self.assertIn("SUBSTITUTION_AFTER_DENIAL", second.reason_codes)
        self.assertEqual(second.intent_ref, "trusted-intent:change-alpha")

    def test_d_agent_relabel_without_resolver_never_allows(self) -> None:
        gateway = make_gateway({self.auth.id: self.auth}, self.target, resolver=None)
        decision = gateway.evaluate(proposal(semantic_action_id="brand-new-agent-label"))
        self.assertNotEqual(decision.decision, Decision.ALLOW)
        self.assertIn("NO_TRUSTED_ACTION_CORRELATION", decision.reason_codes)

    def test_e_binding_proposal_mismatch_denies(self) -> None:
        def bad_resolver(p: ActionProposal) -> ActionIntentBinding:
            binding = trusted_intent(p)
            return ActionIntentBinding(
                id=binding.id,
                issuer=binding.issuer,
                proposal_ref="P-DIFFERENT",
                intent_ref=binding.intent_ref,
                issued_at=binding.issued_at,
                expires_at=binding.expires_at,
                provenance=binding.provenance,
                authority_ref=binding.authority_ref,
            )

        gateway = make_gateway({self.auth.id: self.auth}, self.target, resolver=bad_resolver)
        decision = gateway.evaluate(proposal())
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("ACTION_CORRELATION_PROPOSAL_MISMATCH", decision.reason_codes)

    def test_f_binding_authority_mismatch_denies(self) -> None:
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

    def test_g_expired_binding_denies(self) -> None:
        def expired_resolver(p: ActionProposal) -> ActionIntentBinding:
            return ActionIntentBinding(
                id=f"BIND-{p.id}",
                issuer="trusted-test-orchestrator",
                proposal_ref=p.id,
                intent_ref="trusted-intent:expired",
                issued_at=NOW - timedelta(hours=2),
                expires_at=NOW - timedelta(hours=1),
                provenance="test-fixture-binding",
                authority_ref=p.authority_ref,
            )

        gateway = make_gateway({self.auth.id: self.auth}, self.target, resolver=expired_resolver)
        decision = gateway.evaluate(proposal())
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("ACTION_CORRELATION_EXPIRED", decision.reason_codes)

    def test_g_provenance_free_binding_denies(self) -> None:
        def no_provenance_resolver(p: ActionProposal) -> ActionIntentBinding:
            binding = trusted_intent(p)
            return ActionIntentBinding(
                id=binding.id,
                issuer=binding.issuer,
                proposal_ref=binding.proposal_ref,
                intent_ref=binding.intent_ref,
                issued_at=binding.issued_at,
                expires_at=binding.expires_at,
                provenance="",
                authority_ref=binding.authority_ref,
            )

        gateway = make_gateway({self.auth.id: self.auth}, self.target, resolver=no_provenance_resolver)
        decision = gateway.evaluate(proposal())
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("ACTION_CORRELATION_NO_PROVENANCE", decision.reason_codes)

    def test_h_new_explicit_grant_is_independently_evaluable(self) -> None:
        new_auth = token("AUTH-2")
        gateway = make_gateway({self.auth.id: self.auth, new_auth.id: new_auth}, self.target)
        first = gateway.evaluate(proposal(capability="write", semantic_action_id="change-alpha"))
        self.assertEqual(first.decision, Decision.DENY)

        second = gateway.evaluate(
            proposal(
                proposal_id="P-2",
                authority_ref="AUTH-2",
                semantic_action_id="change-alpha",
            )
        )
        self.assertEqual(second.decision, Decision.ALLOW)

    def test_i_escalation_resolution_is_not_sticky_denial(self) -> None:
        resolver_state = {"ready": False}

        def resolver(p: ActionProposal):
            if not resolver_state["ready"]:
                return None
            return trusted_intent(p, intent_ref="trusted-intent:clarified")

        gateway = make_gateway({self.auth.id: self.auth}, self.target, resolver=resolver)
        first = gateway.evaluate(proposal(proposal_id="P-1", semantic_action_id="agent-label"))
        self.assertEqual(first.decision, Decision.ESCALATE)

        resolver_state["ready"] = True
        second = gateway.evaluate(proposal(proposal_id="P-2", semantic_action_id="renamed-label"))
        self.assertEqual(second.decision, Decision.ALLOW)
        self.assertEqual(second.intent_ref, "trusted-intent:clarified")


if __name__ == "__main__":
    unittest.main()
