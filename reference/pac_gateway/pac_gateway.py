"""Deterministic PAC Authority Gateway reference implementation.

Research-only implementation for controlled sandbox testing.
No network, shell, subprocess, dynamic import, or external execution capability is exposed.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Callable, Mapping, Optional, Sequence


class Decision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    ESCALATE = "ESCALATE"
    DEFER = "DEFER"


class Check(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    ESCALATE = "ESCALATE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    RESTRICTED = "RESTRICTED"
    OPEN = "OPEN"
    RECOVERY = "RECOVERY"


class TargetMatch(str, Enum):
    MATCH_AUTHORIZED = "MATCH_AUTHORIZED"
    MATCH_FORBIDDEN = "MATCH_FORBIDDEN"
    AMBIGUOUS = "AMBIGUOUS"
    NO_MATCH = "NO_MATCH"


@dataclass(frozen=True)
class AuthorityToken:
    id: str
    issuer: str
    subject: str
    issued_at: datetime
    expires_at: datetime
    objective_scope: frozenset[str]
    target_scope_refs: frozenset[str]
    capability_scope: frozenset[str]
    resource_scope: frozenset[str]
    provenance: str
    status: str = "ACTIVE"
    delegation_allowed: bool = False
    max_delegation_depth: int = 0
    parent_authority_ref: Optional[str] = None


@dataclass(frozen=True)
class TargetScope:
    id: str
    identifiers: frozenset[str]
    allowed_effects: frozenset[str]
    forbidden_effects: frozenset[str] = frozenset()
    real_world_effects_allowed: bool = False
    identity_confidence_required: str = "high"
    ambiguity_behavior: str = "DENY_OR_ESCALATE"

    def match(self, identifiers: frozenset[str], *, ambiguous: bool = False) -> TargetMatch:
        if ambiguous:
            return TargetMatch.AMBIGUOUS
        if not identifiers:
            return TargetMatch.NO_MATCH
        if identifiers <= self.identifiers:
            return TargetMatch.MATCH_AUTHORIZED
        return TargetMatch.NO_MATCH


@dataclass(frozen=True)
class DelegationRecord:
    id: str
    parent_authority_ref: str
    delegator: str
    delegatee: str
    issued_at: datetime
    expires_at: datetime
    objective_scope: frozenset[str]
    target_scope_refs: frozenset[str]
    capability_scope: frozenset[str]
    resource_scope: frozenset[str]
    provenance: str
    further_delegation_allowed: bool = False
    remaining_delegation_depth: int = 0
    status: str = "ACTIVE"


@dataclass(frozen=True)
class ArtifactTrustLabel:
    artifact_id: str
    trust_class: str = "UNTRUSTED"
    may_inform_reasoning: bool = True
    may_confer_authority: bool = False
    may_execute: bool = False


@dataclass(frozen=True)
class ActionProposal:
    id: str
    subject: str
    objective: str
    target_scope_ref: str
    target_identifiers: frozenset[str]
    capability: str
    resource: str
    effect: str
    authority_ref: Optional[str]
    semantic_action_id: str
    uncertain_target: bool = False
    authority_claim_artifact_ids: tuple[str, ...] = ()
    peer_support_count: int = 0


@dataclass(frozen=True)
class AuditEvent:
    id: str
    timestamp: datetime
    proposal_ref: str
    subject: str
    decision: Decision
    reason_codes: tuple[str, ...]
    authority_ref: Optional[str]
    checks: Mapping[str, str]


@dataclass(frozen=True)
class GatewayDecision:
    id: str
    timestamp: datetime
    proposal_ref: str
    subject: str
    authority_ref: Optional[str]
    target_scope_ref: str
    checks: Mapping[str, Check]
    decision: Decision
    reason_codes: tuple[str, ...]
    audit_event: AuditEvent


@dataclass
class CircuitBreaker:
    state: CircuitState = CircuitState.CLOSED
    reason: Optional[str] = None

    def restrict(self, reason: str) -> None:
        if self.state == CircuitState.CLOSED:
            self.state = CircuitState.RESTRICTED
        self.reason = reason

    def open(self, reason: str) -> None:
        self.state = CircuitState.OPEN
        self.reason = reason

    def begin_recovery(self, reason: str) -> None:
        if self.state != CircuitState.OPEN:
            raise ValueError("recovery may begin only from OPEN")
        self.state = CircuitState.RECOVERY
        self.reason = reason

    def close(self) -> None:
        self.state = CircuitState.CLOSED
        self.reason = None


class Gateway:
    """PAC authority gateway with fail-closed deterministic checks."""

    def __init__(
        self,
        *,
        authority_tokens: Mapping[str, AuthorityToken],
        target_scopes: Mapping[str, TargetScope],
        artifact_labels: Mapping[str, ArtifactTrustLabel] | None = None,
        delegations: Mapping[str, DelegationRecord] | None = None,
        circuit_breaker: CircuitBreaker | None = None,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self.authority_tokens = dict(authority_tokens)
        self.target_scopes = dict(target_scopes)
        self.artifact_labels = dict(artifact_labels or {})
        self.delegations = dict(delegations or {})
        self.circuit_breaker = circuit_breaker or CircuitBreaker()
        self._now = now or (lambda: datetime.now(timezone.utc))
        self._audit: list[AuditEvent] = []
        # A denial is sticky only under the same authority grant. A new explicit
        # grant can authorize the semantic action without inheriting the old denial.
        self._denied_semantic_actions: set[tuple[str, str, Optional[str]]] = set()
        self._counter = 0

    @property
    def audit_log(self) -> Sequence[AuditEvent]:
        return tuple(self._audit)

    def _next_id(self, prefix: str) -> str:
        self._counter += 1
        return f"{prefix}-{self._counter:06d}"

    @staticmethod
    def _scope_contains(scope: frozenset[str], value: str) -> bool:
        # Missing scope never means wildcard/all.
        return bool(scope) and value in scope

    def validate_delegation(self, record: DelegationRecord) -> tuple[bool, tuple[str, ...]]:
        """Validate a proposed delegation record against its parent token."""
        reasons: list[str] = []
        parent = self.authority_tokens.get(record.parent_authority_ref)
        now = self._now()

        if parent is None:
            reasons.append("NO_PARENT_AUTHORITY")
            return False, tuple(reasons)
        if parent.status != "ACTIVE":
            reasons.append("PARENT_AUTHORITY_REVOKED")
        if not (parent.issued_at <= now <= parent.expires_at):
            reasons.append("PARENT_AUTHORITY_EXPIRED")
        if not parent.delegation_allowed:
            reasons.append("DELEGATION_NOT_ALLOWED")
        if parent.max_delegation_depth < 1:
            reasons.append("DELEGATION_DEPTH_EXHAUSTED")
        if record.status != "ACTIVE":
            reasons.append("DELEGATION_INACTIVE")
        if not record.provenance:
            reasons.append("NO_DELEGATION_PROVENANCE")
        if not record.objective_scope <= parent.objective_scope:
            reasons.append("DELEGATION_EXCEEDS_PARENT_OBJECTIVE")
        if not record.target_scope_refs <= parent.target_scope_refs:
            reasons.append("DELEGATION_EXCEEDS_PARENT_TARGET")
        if not record.capability_scope <= parent.capability_scope:
            reasons.append("DELEGATION_EXCEEDS_PARENT_CAPABILITY")
        if not record.resource_scope <= parent.resource_scope:
            reasons.append("DELEGATION_EXCEEDS_PARENT_RESOURCE")
        if record.remaining_delegation_depth > parent.max_delegation_depth - 1:
            reasons.append("DELEGATION_EXCEEDS_PARENT_DEPTH")
        if not (record.issued_at <= now <= record.expires_at):
            reasons.append("DELEGATION_EXPIRED")
        return not reasons, tuple(reasons)

    def validate_token_lineage(self, token: AuthorityToken) -> tuple[bool, tuple[str, ...]]:
        """Validate delegated token ancestry and subset monotonicity."""
        if not token.parent_authority_ref:
            return True, ()

        reasons: list[str] = []
        seen: set[str] = {token.id}
        child = token
        depth = 0

        while child.parent_authority_ref:
            parent = self.authority_tokens.get(child.parent_authority_ref)
            if parent is None:
                reasons.append("DELEGATION_CHAIN_UNRESOLVED")
                break
            if parent.id in seen:
                reasons.append("DELEGATION_CYCLE")
                break
            seen.add(parent.id)
            depth += 1

            if not parent.delegation_allowed:
                reasons.append("DELEGATION_NOT_ALLOWED")
            if depth > parent.max_delegation_depth:
                reasons.append("DELEGATION_DEPTH_EXHAUSTED")
            if not child.objective_scope <= parent.objective_scope:
                reasons.append("DELEGATION_EXCEEDS_PARENT_OBJECTIVE")
            if not child.target_scope_refs <= parent.target_scope_refs:
                reasons.append("DELEGATION_EXCEEDS_PARENT_TARGET")
            if not child.capability_scope <= parent.capability_scope:
                reasons.append("DELEGATION_EXCEEDS_PARENT_CAPABILITY")
            if not child.resource_scope <= parent.resource_scope:
                reasons.append("DELEGATION_EXCEEDS_PARENT_RESOURCE")
            child = parent

        return not reasons, tuple(dict.fromkeys(reasons))

    def evaluate(self, proposal: ActionProposal) -> GatewayDecision:
        now = self._now()
        checks: dict[str, Check] = {
            "authority_provenance": Check.FAIL,
            "objective_scope": Check.FAIL,
            "target_scope": Check.FAIL,
            "capability_scope": Check.FAIL,
            "resource_scope": Check.FAIL,
            "time_scope": Check.FAIL,
            "delegation_chain": Check.NOT_APPLICABLE,
            "artifact_trust": Check.PASS,
            "circuit_breaker": Check.PASS,
            "uncertainty_policy": Check.PASS,
            "route_substitution": Check.PASS,
        }
        reasons: list[str] = []
        decision = Decision.DENY

        # Emergency state only narrows authority; it never grants privilege.
        if self.circuit_breaker.state == CircuitState.OPEN:
            checks["circuit_breaker"] = Check.FAIL
            reasons.append("CIRCUIT_BREAKER_OPEN")
        elif self.circuit_breaker.state in {CircuitState.RESTRICTED, CircuitState.RECOVERY}:
            checks["circuit_breaker"] = Check.ESCALATE
            reasons.append("CIRCUIT_BREAKER_RESTRICTED")

        # Uncertainty cannot expand authority.
        if proposal.uncertain_target:
            checks["uncertainty_policy"] = Check.ESCALATE
            reasons.append("UNCERTAINTY_REQUIRES_ESCALATION")

        # Artifacts may inform reasoning but cannot serve as the authority source.
        if proposal.authority_claim_artifact_ids:
            checks["artifact_trust"] = Check.FAIL
            reasons.append("UNTRUSTED_ARTIFACT_DEPENDENCY")

        # Peer consensus is deliberately not an authorization input.
        _ = proposal.peer_support_count

        token = self.authority_tokens.get(proposal.authority_ref or "")
        if token is None:
            reasons.append("NO_AUTHORITY_PROVENANCE")
        else:
            if token.provenance:
                checks["authority_provenance"] = Check.PASS
            else:
                reasons.append("NO_AUTHORITY_PROVENANCE")

            if token.status != "ACTIVE":
                reasons.append("AUTHORITY_REVOKED")
            elif token.issued_at <= now <= token.expires_at:
                checks["time_scope"] = Check.PASS
            else:
                reasons.append("AUTHORITY_EXPIRED")

            if token.subject != proposal.subject:
                reasons.append("AUTHORITY_SUBJECT_MISMATCH")
            elif self._scope_contains(token.objective_scope, proposal.objective):
                checks["objective_scope"] = Check.PASS
            else:
                reasons.append("OBJECTIVE_OUT_OF_SCOPE")

            if self._scope_contains(token.capability_scope, proposal.capability):
                checks["capability_scope"] = Check.PASS
            else:
                reasons.append("CAPABILITY_OUT_OF_SCOPE")

            if self._scope_contains(token.resource_scope, proposal.resource):
                checks["resource_scope"] = Check.PASS
            else:
                reasons.append("RESOURCE_OUT_OF_SCOPE")

            if proposal.target_scope_ref in token.target_scope_refs:
                target = self.target_scopes.get(proposal.target_scope_ref)
                if target is None:
                    reasons.append("TARGET_SCOPE_UNRESOLVED")
                else:
                    match = target.match(
                        proposal.target_identifiers,
                        ambiguous=proposal.uncertain_target,
                    )
                    if match == TargetMatch.MATCH_AUTHORIZED:
                        if proposal.effect in target.forbidden_effects:
                            reasons.append("TARGET_EFFECT_FORBIDDEN")
                        elif proposal.effect not in target.allowed_effects:
                            reasons.append("TARGET_EFFECT_NOT_AUTHORIZED")
                        else:
                            checks["target_scope"] = Check.PASS
                    elif match == TargetMatch.AMBIGUOUS:
                        reasons.append("TARGET_AMBIGUOUS")
                        checks["target_scope"] = Check.ESCALATE
                    else:
                        reasons.append("TARGET_NOT_AUTHORIZED")
            else:
                reasons.append("TARGET_NOT_AUTHORIZED")

            lineage_ok, lineage_reasons = self.validate_token_lineage(token)
            if token.parent_authority_ref:
                checks["delegation_chain"] = Check.PASS if lineage_ok else Check.FAIL
            reasons.extend(lineage_reasons)

        denial_key = (proposal.subject, proposal.semantic_action_id, proposal.authority_ref)
        if denial_key in self._denied_semantic_actions:
            checks["route_substitution"] = Check.FAIL
            reasons.append("SUBSTITUTION_AFTER_DENIAL")

        mandatory = (
            "authority_provenance",
            "objective_scope",
            "target_scope",
            "capability_scope",
            "resource_scope",
            "time_scope",
            "artifact_trust",
            "circuit_breaker",
            "uncertainty_policy",
            "route_substitution",
        )

        if not reasons and all(checks[name] == Check.PASS for name in mandatory):
            decision = Decision.ALLOW
        elif any(checks[name] == Check.ESCALATE for name in mandatory):
            decision = Decision.ESCALATE
        else:
            decision = Decision.DENY

        if decision in {Decision.DENY, Decision.ESCALATE}:
            self._denied_semantic_actions.add(denial_key)

        audit = AuditEvent(
            id=self._next_id("AUD"),
            timestamp=now,
            proposal_ref=proposal.id,
            subject=proposal.subject,
            decision=decision,
            reason_codes=tuple(dict.fromkeys(reasons)),
            authority_ref=proposal.authority_ref,
            checks={k: v.value for k, v in checks.items()},
        )
        self._audit.append(audit)

        return GatewayDecision(
            id=self._next_id("GWD"),
            timestamp=now,
            proposal_ref=proposal.id,
            subject=proposal.subject,
            authority_ref=proposal.authority_ref,
            target_scope_ref=proposal.target_scope_ref,
            checks=checks,
            decision=decision,
            reason_codes=audit.reason_codes,
            audit_event=audit,
        )
