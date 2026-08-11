"""Aggregate plan authority for PAC multi-agent sandbox experiments.

This layer prevents individually authorized substeps from silently composing into
an aggregate effect beyond a trusted plan envelope.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Callable, Mapping, Optional

from .pac_gateway import ActionProposal, Decision, GatewayDecision


@dataclass(frozen=True)
class PlanEnvelope:
    id: str
    issuer: str
    created_at: datetime
    expires_at: datetime
    objective: str
    subjects: frozenset[str]
    authorized_authority_refs: Mapping[str, frozenset[str]]
    target_scope_refs: frozenset[str]
    allowed_capabilities: frozenset[str]
    allowed_resources: frozenset[str]
    allowed_effects: frozenset[str]
    step_limit: int
    resource_budgets: Mapping[str, int]
    effect_budgets: Mapping[str, int]
    provenance: str
    status: str = "ACTIVE"


@dataclass(frozen=True)
class PlanStep:
    id: str
    plan_ref: str
    proposal: ActionProposal
    resource_units: int = 1
    effect_units: int = 1


@dataclass(frozen=True)
class PlanDecision:
    step_ref: str
    plan_ref: str
    decision: Decision
    reason_codes: tuple[str, ...]
    step_count_after: int
    resource_usage_after: Mapping[str, int]
    effect_usage_after: Mapping[str, int]
    subject_step_count_after: Mapping[str, int]


@dataclass(frozen=True)
class PlanSnapshot:
    plan_ref: str
    step_count: int
    resource_usage: Mapping[str, int]
    effect_usage: Mapping[str, int]
    subject_step_count: Mapping[str, int]


@dataclass
class _PlanState:
    step_count: int = 0
    resource_usage: dict[str, int] = field(default_factory=dict)
    effect_usage: dict[str, int] = field(default_factory=dict)
    subject_step_count: dict[str, int] = field(default_factory=dict)


class PlanLedger:
    """Trusted registry plus atomic local aggregate-budget evaluator."""

    def __init__(
        self,
        *,
        plans: Mapping[str, PlanEnvelope],
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self.plans = dict(plans)
        self._states = {plan_id: _PlanState() for plan_id in self.plans}
        self._now = now or (lambda: datetime.now(timezone.utc))
        self._lock = Lock()

    def snapshot(self, plan_ref: str) -> Optional[PlanSnapshot]:
        """Return a copy of aggregate state without overloading decision semantics."""
        with self._lock:
            state = self._states.get(plan_ref)
            if state is None:
                return None
            return PlanSnapshot(
                plan_ref=plan_ref,
                step_count=state.step_count,
                resource_usage=dict(state.resource_usage),
                effect_usage=dict(state.effect_usage),
                subject_step_count=dict(state.subject_step_count),
            )

    def evaluate_and_commit(
        self,
        step: PlanStep,
        local_decision: GatewayDecision,
    ) -> PlanDecision:
        """Evaluate one already-gated substep and atomically reserve its budget."""
        with self._lock:
            reasons: list[str] = []
            plan = self.plans.get(step.plan_ref)

            if local_decision.proposal_ref != step.proposal.id:
                reasons.append("LOCAL_DECISION_PROPOSAL_MISMATCH")
            if local_decision.decision != Decision.ALLOW:
                reasons.append("LOCAL_GATEWAY_NOT_ALLOW")

            if plan is None:
                return self._decision(step, Decision.DENY, ("PLAN_NOT_FOUND",) + tuple(reasons))

            state = self._states[plan.id]
            now = self._now()
            proposal = step.proposal

            if plan.status != "ACTIVE":
                reasons.append("PLAN_INACTIVE")
            if not plan.provenance:
                reasons.append("PLAN_PROVENANCE_MISSING")
            if not (plan.created_at <= now <= plan.expires_at):
                reasons.append("PLAN_EXPIRED")
            if proposal.objective != plan.objective:
                reasons.append("PLAN_OBJECTIVE_MISMATCH")
            if proposal.subject not in plan.subjects:
                reasons.append("PLAN_SUBJECT_NOT_AUTHORIZED")

            subject_authorities = plan.authorized_authority_refs.get(proposal.subject, frozenset())
            if not subject_authorities:
                reasons.append("PLAN_SUBJECT_AUTHORITY_NOT_BOUND")
            elif proposal.authority_ref not in subject_authorities:
                reasons.append("PLAN_AUTHORITY_MISMATCH")

            if proposal.target_scope_ref not in plan.target_scope_refs:
                reasons.append("PLAN_TARGET_NOT_AUTHORIZED")
            if proposal.capability not in plan.allowed_capabilities:
                reasons.append("PLAN_CAPABILITY_NOT_AUTHORIZED")
            if proposal.resource not in plan.allowed_resources:
                reasons.append("PLAN_RESOURCE_NOT_AUTHORIZED")
            if proposal.effect not in plan.allowed_effects:
                reasons.append("PLAN_EFFECT_NOT_AUTHORIZED")
            if step.resource_units < 0 or step.effect_units < 0:
                reasons.append("NEGATIVE_BUDGET_UNITS_INVALID")

            next_step_count = state.step_count + 1
            if plan.step_limit < 0 or next_step_count > plan.step_limit:
                reasons.append("PLAN_STEP_LIMIT_EXCEEDED")

            resource_budget = plan.resource_budgets.get(proposal.resource)
            if resource_budget is None:
                reasons.append("PLAN_RESOURCE_BUDGET_MISSING")
            else:
                next_resource = state.resource_usage.get(proposal.resource, 0) + step.resource_units
                if next_resource > resource_budget:
                    reasons.append("PLAN_RESOURCE_BUDGET_EXCEEDED")

            effect_budget = plan.effect_budgets.get(proposal.effect)
            if effect_budget is None:
                reasons.append("PLAN_EFFECT_BUDGET_MISSING")
            else:
                next_effect = state.effect_usage.get(proposal.effect, 0) + step.effect_units
                if next_effect > effect_budget:
                    reasons.append("PLAN_EFFECT_BUDGET_EXCEEDED")

            if reasons:
                return self._decision(step, Decision.DENY, tuple(dict.fromkeys(reasons)))

            # Commit only after every local and aggregate check passes. The lock
            # makes evaluation + reservation atomic within this process.
            state.step_count = next_step_count
            state.resource_usage[proposal.resource] = (
                state.resource_usage.get(proposal.resource, 0) + step.resource_units
            )
            state.effect_usage[proposal.effect] = (
                state.effect_usage.get(proposal.effect, 0) + step.effect_units
            )
            state.subject_step_count[proposal.subject] = (
                state.subject_step_count.get(proposal.subject, 0) + 1
            )
            return self._decision(step, Decision.ALLOW, ())

    def _decision(
        self,
        step: PlanStep,
        decision: Decision,
        reasons: tuple[str, ...],
    ) -> PlanDecision:
        state = self._states.get(step.plan_ref, _PlanState())
        return PlanDecision(
            step_ref=step.id,
            plan_ref=step.plan_ref,
            decision=decision,
            reason_codes=reasons,
            step_count_after=state.step_count,
            resource_usage_after=dict(state.resource_usage),
            effect_usage_after=dict(state.effect_usage),
            subject_step_count_after=dict(state.subject_step_count),
        )
