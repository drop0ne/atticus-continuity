from __future__ import annotations

import unittest
from datetime import datetime, timedelta, timezone
from threading import Barrier, Thread

from .pac_gateway import (
    ActionIntentBinding,
    ActionProposal,
    AuthorityToken,
    Decision,
    Gateway,
    TargetScope,
)
from .plan import PlanEnvelope, PlanLedger, PlanSnapshot, PlanStep


NOW = datetime(2026, 8, 11, 23, 0, tzinfo=timezone.utc)


def trusted_intent(proposal: ActionProposal) -> ActionIntentBinding:
    return ActionIntentBinding(
        id=f"BIND-{proposal.id}",
        issuer="trusted-plan-test-orchestrator",
        proposal_ref=proposal.id,
        intent_ref=proposal.semantic_action_id,
        issued_at=NOW - timedelta(minutes=1),
        expires_at=NOW + timedelta(minutes=10),
        provenance="trusted-plan-test-binding",
        authority_ref=proposal.authority_ref,
    )


def make_authority(token_id: str, subject: str) -> AuthorityToken:
    return AuthorityToken(
        id=token_id,
        issuer="test-authority",
        subject=subject,
        issued_at=NOW - timedelta(minutes=5),
        expires_at=NOW + timedelta(hours=1),
        objective_scope=frozenset({"inspect-sim"}),
        target_scope_refs=frozenset({"TGT-PLAN-1"}),
        capability_scope=frozenset({"read"}),
        resource_scope=frozenset({"sim-db"}),
        provenance=f"plan-test-authority:{subject}",
    )


def build_components(*, step_limit=2, budget=2):
    authorities = {
        "AUTH-PLAN-A": make_authority("AUTH-PLAN-A", "agent-a"),
        "AUTH-PLAN-B": make_authority("AUTH-PLAN-B", "agent-b"),
    }
    target = TargetScope(
        id="TGT-PLAN-1",
        identifiers=frozenset({"sim://plan/alpha"}),
        allowed_effects=frozenset({"observe"}),
    )
    gateway = Gateway(
        authority_tokens=authorities,
        target_scopes={target.id: target},
        intent_resolver=trusted_intent,
        now=lambda: NOW,
    )
    plan = PlanEnvelope(
        id="PLAN-1",
        issuer="trusted-orchestrator",
        created_at=NOW - timedelta(minutes=1),
        expires_at=NOW + timedelta(minutes=30),
        objective="inspect-sim",
        subjects=frozenset({"agent-a", "agent-b"}),
        authorized_authority_refs={
            "agent-a": frozenset({"AUTH-PLAN-A"}),
            "agent-b": frozenset({"AUTH-PLAN-B"}),
        },
        target_scope_refs=frozenset({"TGT-PLAN-1"}),
        allowed_capabilities=frozenset({"read"}),
        allowed_resources=frozenset({"sim-db"}),
        allowed_effects=frozenset({"observe"}),
        step_limit=step_limit,
        resource_budgets={"sim-db": budget},
        effect_budgets={"observe": budget},
        provenance="trusted-plan-record",
    )
    ledger = PlanLedger(plans={plan.id: plan}, now=lambda: NOW)
    return authorities, target, gateway, plan, ledger


def make_proposal(
    proposal_id: str,
    *,
    subject="agent-a",
    authority_ref: str | None = None,
):
    if authority_ref is None:
        authority_ref = "AUTH-PLAN-A" if subject == "agent-a" else "AUTH-PLAN-B"
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

    def test_snapshot_has_dedicated_type(self) -> None:
        _, _, gateway, _, ledger = build_components()
        p = make_proposal("P-1")
        ledger.evaluate_and_commit(PlanStep("STEP-1", "PLAN-1", p), gateway.evaluate(p))
        snapshot = ledger.snapshot("PLAN-1")
        self.assertIsInstance(snapshot, PlanSnapshot)
        self.assertEqual(snapshot.step_count, 1)
        self.assertEqual(snapshot.subject_step_count["agent-a"], 1)

    def test_step_budget_blocks_third_substep(self) -> None:
        _, _, gateway, _, ledger = build_components(step_limit=2, budget=10)
        for index in range(2):
            p = make_proposal(f"P-{index}")
            aggregate = ledger.evaluate_and_commit(
                PlanStep(f"STEP-{index}", "PLAN-1", p), gateway.evaluate(p)
            )
            self.assertEqual(aggregate.decision, Decision.ALLOW)

        p3 = make_proposal("P-3")
        aggregate3 = ledger.evaluate_and_commit(PlanStep("STEP-3", "PLAN-1", p3), gateway.evaluate(p3))
        self.assertEqual(aggregate3.decision, Decision.DENY)
        self.assertIn("PLAN_STEP_LIMIT_EXCEEDED", aggregate3.reason_codes)

    def test_effect_and_resource_budgets_persist_across_steps(self) -> None:
        _, _, gateway, _, ledger = build_components(step_limit=10, budget=2)
        for index in range(2):
            p = make_proposal(f"P-{index}")
            aggregate = ledger.evaluate_and_commit(
                PlanStep(f"STEP-{index}", "PLAN-1", p), gateway.evaluate(p)
            )
            self.assertEqual(aggregate.decision, Decision.ALLOW)

        p3 = make_proposal("P-3")
        aggregate3 = ledger.evaluate_and_commit(PlanStep("STEP-3", "PLAN-1", p3), gateway.evaluate(p3))
        self.assertEqual(aggregate3.decision, Decision.DENY)
        self.assertIn("PLAN_RESOURCE_BUDGET_EXCEEDED", aggregate3.reason_codes)
        self.assertIn("PLAN_EFFECT_BUDGET_EXCEEDED", aggregate3.reason_codes)

    def test_aggregate_budget_persists_across_independent_agents(self) -> None:
        _, _, gateway, _, ledger = build_components(step_limit=10, budget=2)

        pa = make_proposal("P-A", subject="agent-a")
        pb = make_proposal("P-B", subject="agent-b")
        self.assertEqual(
            ledger.evaluate_and_commit(PlanStep("STEP-A", "PLAN-1", pa), gateway.evaluate(pa)).decision,
            Decision.ALLOW,
        )
        self.assertEqual(
            ledger.evaluate_and_commit(PlanStep("STEP-B", "PLAN-1", pb), gateway.evaluate(pb)).decision,
            Decision.ALLOW,
        )

        pc = make_proposal("P-C", subject="agent-a")
        third = ledger.evaluate_and_commit(PlanStep("STEP-C", "PLAN-1", pc), gateway.evaluate(pc))
        self.assertEqual(third.decision, Decision.DENY)
        self.assertIn("PLAN_RESOURCE_BUDGET_EXCEEDED", third.reason_codes)
        snapshot = ledger.snapshot("PLAN-1")
        self.assertEqual(snapshot.subject_step_count, {"agent-a": 1, "agent-b": 1})

    def test_agent_cannot_use_another_subjects_plan_authority_binding(self) -> None:
        _, _, gateway, _, ledger = build_components()
        p = make_proposal("P-X", subject="agent-b", authority_ref="AUTH-PLAN-A")
        local = gateway.evaluate(p)
        aggregate = ledger.evaluate_and_commit(PlanStep("STEP-X", "PLAN-1", p), local)
        self.assertEqual(aggregate.decision, Decision.DENY)
        self.assertIn("LOCAL_GATEWAY_NOT_ALLOW", aggregate.reason_codes)
        self.assertIn("PLAN_AUTHORITY_MISMATCH", aggregate.reason_codes)

    def test_local_denial_cannot_be_repaired_by_plan(self) -> None:
        _, _, gateway, _, ledger = build_components()
        p = make_proposal("P-1", authority_ref="AUTH-NOT-REGISTERED")
        local = gateway.evaluate(p)
        aggregate = ledger.evaluate_and_commit(PlanStep("STEP-1", "PLAN-1", p), local)
        self.assertEqual(local.decision, Decision.DENY)
        self.assertEqual(aggregate.decision, Decision.DENY)
        self.assertIn("LOCAL_GATEWAY_NOT_ALLOW", aggregate.reason_codes)

    def test_plan_authority_mismatch_denies(self) -> None:
        _, _, gateway, _, ledger = build_components()
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
        self.assertIsNone(ledger.snapshot("PLAN-UNKNOWN"))

    def test_concurrent_final_budget_reservation_allows_at_most_one(self) -> None:
        _, _, gateway, _, ledger = build_components(step_limit=10, budget=1)
        pa = make_proposal("P-A", subject="agent-a")
        pb = make_proposal("P-B", subject="agent-b")
        local_a = gateway.evaluate(pa)
        local_b = gateway.evaluate(pb)
        self.assertEqual(local_a.decision, Decision.ALLOW)
        self.assertEqual(local_b.decision, Decision.ALLOW)

        barrier = Barrier(3)
        decisions = []
        errors = []

        def worker(step, local):
            try:
                barrier.wait()
                decisions.append(ledger.evaluate_and_commit(step, local))
            except BaseException as exc:  # captured so the test can report thread failures
                errors.append(exc)

        threads = [
            Thread(target=worker, args=(PlanStep("STEP-A", "PLAN-1", pa), local_a)),
            Thread(target=worker, args=(PlanStep("STEP-B", "PLAN-1", pb), local_b)),
        ]
        for thread in threads:
            thread.start()
        barrier.wait()
        for thread in threads:
            thread.join()

        self.assertEqual(errors, [])
        self.assertEqual(sum(d.decision == Decision.ALLOW for d in decisions), 1)
        self.assertEqual(sum(d.decision == Decision.DENY for d in decisions), 1)
        snapshot = ledger.snapshot("PLAN-1")
        self.assertEqual(snapshot.step_count, 1)
        self.assertEqual(snapshot.resource_usage["sim-db"], 1)
        self.assertEqual(snapshot.effect_usage["observe"], 1)


if __name__ == "__main__":
    unittest.main()
