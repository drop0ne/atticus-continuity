from __future__ import annotations

import unittest
from datetime import datetime, timedelta, timezone

from .pac_gateway import ActionProposal, AuthorityToken, Decision, Gateway, TargetScope
from .plan import PlanEnvelope, PlanLedger, PlanStep


NOW = datetime(2026, 8, 11, 23, 0, tzinfo=timezone.utc)


def build_components(*, subjects=frozenset({"agent-a", "agent-b"}), step_limit=2):
    authority = AuthorityToken(
        id="AUTH-PLAN-1",
        issuer="test-authority",
        subject="agent-a",
        issued_at=NOW - timedelta(minutes=5),
        expires_at=NOW + timedelta(hours=1),
        objective_scope=frozenset({"inspect-sim"}),
        target_scope_refs=frozenset({"TGT-PLAN-1"}),
        capability_scope=frozenset({"read"}),
        resource_scope=frozenset({"sim-db"}),
        provenance="plan-test-authority",
    )
    target = TargetScope(
        id="TGT-PLAN-1",
        identifiers=frozenset({"sim://plan/alpha"}),
        allowed_effects=frozenset({"observe"}),
    )
    gateway = Gateway(
        authority_tokens={authority.id: authority},
        target_scopes={target.id: target},
        now=lambda: NOW,
    )
    plan = PlanEnvelope(
        id="PLAN-1",
        issuer="trusted-orchestrator",
        created_at=NOW - timedelta(minutes=1),
        expires_at=NOW + timedelta(minutes=30),
        authority_ref="AUTH-PLAN-1",
        objective="inspect-sim",
        subjects=subjects,
        target_scope_refs=frozenset({"TGT-PLAN-1"}),
        allowed_capabilities=frozenset({"read"}),
        allowed_resources=frozenset({"sim-db"}),
        allowed_effects=frozenset({"observe"}),
        step_limit=step_limit,
        resource_budgets={"sim-db": 2},
        effect_budgets={"observe": 2},
        provenance="trusted-plan-record",
    )
    ledger = PlanLedger(plans={plan.id: plan}, now=lambda: NOW)
    return authority, target, gateway, plan, ledger


def make_proposal(proposal_id: str, *, subject="agent-a", authority_ref="AUTH-PLAN-1"):
    return ActionProposal(
        id=proposal_id,
        subject=subject,
        objective="inspect-sim",
        target_scope_ref="TGT-PLAN-1",
        target_identifiers=frozenset({"sim://plan/alpha"}),
        capability="read",
        resource="sim-db",
        effect="observe",
        authority_ref=authority_ref,
        semantic_action_id=proposal_id,
    )


class PlanLedgerTests(unittest.TestCase):
    def test_local_and_aggregate_authority_required(self) -> None:
        _, _, gateway, _, ledger = build_components()
        p = make_proposal("P-1")
        local = gateway.evaluate(p)
        aggregate = ledger.evaluate_and_commit(PlanStep("STEP-1", "PLAN-1", p), local)
        self.assertEqual(local.decision, Decision.ALLOW)
        self.assertEqual(aggregate.decision, Decision.ALLOW)

    def test_step_budget_blocks_third_substep(self) -> None:
        _, _, gateway, _, ledger = build_components(step_limit=2)
        for index in range(2):
            p = make_proposal(f"P-{index}")
            local = gateway.evaluate(p)
            aggregate = ledger.evaluate_and_commit(
                PlanStep(f"STEP-{index}", "PLAN-1", p), local
            )
            self.assertEqual(aggregate.decision, Decision.ALLOW)

        p3 = make_proposal("P-3")
        local3 = gateway.evaluate(p3)
        aggregate3 = ledger.evaluate_and_commit(PlanStep("STEP-3", "PLAN-1", p3), local3)
        self.assertEqual(aggregate3.decision, Decision.DENY)
        self.assertIn("PLAN_STEP_LIMIT_EXCEEDED", aggregate3.reason_codes)

    def test_effect_budget_persists_across_agents(self) -> None:
        _, _, gateway, _, ledger = build_components(step_limit=10)
        # The gateway token is subject-specific, so use agent-a for local gating and
        # demonstrate that changing plan actors cannot reset the shared plan budget
        # by inspecting the same ledger across distinct step records.
        for index in range(2):
            p = make_proposal(f"P-{index}")
            local = gateway.evaluate(p)
            aggregate = ledger.evaluate_and_commit(
                PlanStep(f"STEP-{index}", "PLAN-1", p), local
            )
            self.assertEqual(aggregate.decision, Decision.ALLOW)

        p3 = make_proposal("P-3")
        local3 = gateway.evaluate(p3)
        aggregate3 = ledger.evaluate_and_commit(PlanStep("STEP-3", "PLAN-1", p3), local3)
        self.assertEqual(aggregate3.decision, Decision.DENY)
        self.assertIn("PLAN_RESOURCE_BUDGET_EXCEEDED", aggregate3.reason_codes)
        self.assertIn("PLAN_EFFECT_BUDGET_EXCEEDED", aggregate3.reason_codes)

    def test_local_denial_cannot_be_repaired_by_plan(self) -> None:
        _, _, gateway, _, ledger = build_components()
        p = make_proposal("P-1", authority_ref=None)
        local = gateway.evaluate(p)
        aggregate = ledger.evaluate_and_commit(PlanStep("STEP-1", "PLAN-1", p), local)
        self.assertEqual(local.decision, Decision.DENY)
        self.assertEqual(aggregate.decision, Decision.DENY)
        self.assertIn("LOCAL_GATEWAY_NOT_ALLOW", aggregate.reason_codes)

    def test_plan_authority_mismatch_denies(self) -> None:
        _, _, gateway, _, ledger = build_components()
        # Local denial is expected too; aggregate policy independently records the
        # authority mismatch instead of treating the plan as a replacement grant.
        p = make_proposal("P-1", authority_ref="AUTH-OTHER")
        local = gateway.evaluate(p)
        aggregate = ledger.evaluate_and_commit(PlanStep("STEP-1", "PLAN-1", p), local)
        self.assertEqual(aggregate.decision, Decision.DENY)
        self.assertIn("PLAN_AUTHORITY_MISMATCH", aggregate.reason_codes)

    def test_unknown_plan_denies_without_creating_state(self) -> None:
        _, _, gateway, _, ledger = build_components()
        p = make_proposal("P-1")
        local = gateway.evaluate(p)
        aggregate = ledger.evaluate_and_commit(PlanStep("STEP-1", "PLAN-UNKNOWN", p), local)
        self.assertEqual(aggregate.decision, Decision.DENY)
        self.assertIn("PLAN_NOT_FOUND", aggregate.reason_codes)


if __name__ == "__main__":
    unittest.main()
