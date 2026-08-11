"""Inert constrained executor for PAC gateway experiments.

The executor records approved synthetic actions only. It intentionally exposes no
network, filesystem mutation, shell, subprocess, browser, package-manager, or
third-party integration capability.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Sequence

from .pac_gateway import ActionProposal, Decision, GatewayDecision


@dataclass(frozen=True)
class ExecutionRecord:
    id: str
    timestamp: datetime
    proposal_ref: str
    decision_ref: str
    subject: str
    capability: str
    resource: str
    target_scope_ref: str
    effect: str
    result: str


class ConstrainedExecutor:
    """Executes only synthetic state transitions approved by the gateway."""

    def __init__(self, *, now: Callable[[], datetime] | None = None) -> None:
        self._now = now or (lambda: datetime.now(timezone.utc))
        self._records: list[ExecutionRecord] = []
        self._counter = 0

    @property
    def records(self) -> Sequence[ExecutionRecord]:
        return tuple(self._records)

    def execute(self, proposal: ActionProposal, decision: GatewayDecision) -> ExecutionRecord:
        if decision.proposal_ref != proposal.id:
            raise PermissionError("decision does not correspond to proposal")
        if decision.decision != Decision.ALLOW:
            raise PermissionError(f"gateway decision is {decision.decision.value}, not ALLOW")

        self._counter += 1
        record = ExecutionRecord(
            id=f"EXE-{self._counter:06d}",
            timestamp=self._now(),
            proposal_ref=proposal.id,
            decision_ref=decision.id,
            subject=proposal.subject,
            capability=proposal.capability,
            resource=proposal.resource,
            target_scope_ref=proposal.target_scope_ref,
            effect=proposal.effect,
            result="SIMULATED_EFFECT_RECORDED",
        )
        self._records.append(record)
        return record
