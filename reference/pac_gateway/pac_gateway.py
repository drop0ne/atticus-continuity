"""Deterministic PAC Authority Gateway reference implementation.

Research-only implementation for controlled sandbox testing. The module exposes
no network, shell, subprocess, dynamic-import, browser, or external execution
capability.
"""

from __future__ import annotations

import hashlib
import json
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
    # This is an agent-side descriptive hint only, never the trusted security key.
    semantic_action_id: str
    uncertain_target: bool = False
    real_world_effect: bool = False
    authority_claim_artifact_ids: tuple[str, ...] = ()
    peer_support_count: int = 0


@dataclass(frozen=True)
class ActionIntentBinding:
    id: str
    issuer: str
    proposal_ref: str
    intent_ref: str
    issued_at: datetime
    expires_at: datetime
    provenance: str
    authority_ref: Optional[str] = None
    status: str = "ACTIVE"


@dataclass(frozen=True)
class AuditEvent:
    id: str
    timestamp: datetime
    proposal_ref: str
    subject: str
    decision: Decision
    reason_codes: tuple[str, ...]
    authority_ref: Optional[str]
    intent_ref: Optional[str]
    checks: Mapping[str, str]
    previous_event_hash: str
    event_hash: str


@dataclass(frozen=True)
class GatewayDecision:
    id: str
    timestamp: datetime
    proposal_ref: str
    subject: str
    authority_ref: Optional[str]
    target_scope_ref: str
    intent_ref: Optional[str]
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
    """PAC authority gateway with explicit fail-closed pre-action checks."""

    def __init__(
        self,
        *,
        authority_tokens: Mapping[str, AuthorityToken],
        target_scopes: Mapping[str, TargetScope],
        artifact_labels: Mapping[str, ArtifactTrustLabel] | None = None,
        delegations: Mapping[str, DelegationRecord] | None = None,
        circuit_breaker: CircuitBreaker | None = None,
        intent_resolver: Callable[[ActionProposal], Optional[ActionIntentBinding]] | None = None,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self.authority_tokens = dict(authority_tokens)
        self.target_scopes = dict(target_scopes)
        self.artifact_labels = dict(artifact_labels or {})
        self.delegations = dict(delegations or {})
        self.circuit_breaker = circuit_breaker or CircuitBreaker()
        self._intent_resolver = intent_resolver
        self._now = now or (lambda: datetime.now(timezone.utc))
        self._audit: list[AuditEvent] = []
        self._denied_intents: set[tuple[str, str, Optional[str]]] = set()
        self._counter = 0

    @property
    def audit_log(self) -> Sequence[AuditEvent]:
        return tuple(self._audit)

    def _next_id(self, prefix: str) -> str:
        self._counter += 1
        return f"{prefix}-{self._counter:06d}"

    @staticmethod
    def _scope_contains(scope: frozenset[str], value: str) -> bool:
        return bool(scope) and value in scope

    @staticmethod
    def _hash_audit_payload(
        event_id: str,
        timestamp: datetime,
        proposal_ref: str,
        subject: str,
        decision: Decision,
        reason_codes: tuple[str, ...],
        authority_ref: Optional[str],
        intent_ref: Optional[str],
        checks: Mapping[str, str],
        previous_event_hash: str,
    ) -> str:
        payload = {
            "id": event_id,
            "timestamp": timestamp.isoformat(),
            "proposal_ref": proposal_ref,
            "subject": subject,
            "decision": decision.value,
            "reason_codes": list(reason_codes),
            "authority_ref": authority_ref,
            "intent_ref": intent_ref,
            "checks": dict(sorted(checks.items())),
            "previous_event_hash": previous_event_hash,
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def verify_audit_chain(self) -> bool:
        previous = "GENESIS"
        for event in self._audit:
            if event.previous_event_hash != previous:
                return False
            expected = self._hash_audit_payload(
                event.id,
                event.timestamp,
                event.proposal_ref,
                event.subject,
                event.decision,
                event.reason_codes,
                event.authority_ref,
                event.intent_ref,
                event.checks,
                event.previous_event_hash,
            )
            if event.event_hash != expected:
                return False
            previous = event.event_hash
        return True

    def _resolve_intent(
        self, proposal: ActionProposal, now: datetime
    ) -> tuple[Optional[ActionIntentBinding], Check, tuple[str, ...]]:
        if self._intent_resolver is None:
            return None, Check.ESCALATE, ("NO_TRUSTED_ACTION_CORRELATION",)

        binding = self._intent_resolver(proposal)
        if binding is None:
            return None, Check.ESCALATE, ("NO_TRUSTED_ACTION_CORRELATION",)

        reasons: list[str] = []
        if binding.status != "ACTIVE":
            reasons.append("ACTION_CORRELATION_INACTIVE")
        if not binding.provenance:
            reasons.append("ACTION_CORRELATION_NO_PROVENANCE")
        if not binding.intent_ref:
            reasons.append("ACTION_CORRELATION_EMPTY_INTENT")
        if binding.proposal_ref != proposal.id:
            reasons.append("ACTION_CORRELATION_PROPOSAL_MISMATCH")
        if binding.authority_ref != proposal.authority_ref:
            reasons.append("ACTION_CORRELATION_AUTHORITY_MISMATCH")
        if not (binding.issued_at <= now <= binding.expires_at):
            reasons.append("ACTION_CORRELATION_EXPIRED")
        return binding, Check.FAIL if reasons else Check.PASS, tuple(reasons)

    def validate_delegation(self, record: DelegationRecord) -> tuple[bool, tuple[str, ...]]:
        reasons: list[str] = []
        parent = self.authority_tokens.get(record.parent_authority_ref)
        now = self._now()
        if parent is None:
            return False, ("NO_PARENT_AUTHORITY",)
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
        if not token.parent_authority_ref:
            return True, ()
        reasons: list[str] = []
        seen = {token.id}
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
            "trusted_correlation": Check.FAIL,
            "route_substitution": Check.PASS,
            "real_world_effect": Check.PASS,
        }
        reasons: list[str] = []

        binding, correlation_check, correlation_reasons = self._resolve_intent(proposal, now)
        checks["trusted_correlation"] = correlation_check
        reasons.extend(correlation_reasons)
        intent_ref = binding.intent_ref if binding and binding.intent_ref else None

        if self.circuit_breaker.state == CircuitState.OPEN:
            checks["circuit_breaker"] = Check.FAIL
            reasons.append("CIRCUIT_BREAKER_OPEN")
        elif self.circuit_breaker.state in {CircuitState.RESTRICTED, CircuitState.RECOVERY}:
            checks["circuit_breaker"] = Check.ESCALATE
            reasons.append("CIRCUIT_BREAKER_RESTRICTED")

        if proposal.uncertain_target:
            checks["uncertainty_policy"] = Check.ESCALATE
            reasons.append("UNCERTAINTY_REQUIRES_ESCALATION")

        if proposal.authority_claim_artifact_ids:
            checks["artifact_trust"] = Check.FAIL
            reasons.append("UNTRUSTED_ARTIFACT_DEPENDENCY")

        # Peer support is observable context, never an authorization input.
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

            if proposal.target_scope_ref not in token.target_scope_refs:
                reasons.append("TARGET_NOT_AUTHORIZED")
            else:
                target = self.target_scopes.get(proposal.target_scope_ref)
                if target is None:
                    reasons.append("TARGET_SCOPE_UNRESOLVED")
                else:
                    if proposal.real_world_effect and not target.real_world_effects_allowed:
                        checks["real_world_effect"] = Check.FAIL
                        reasons.append("REAL_WORLD_EFFECT_NOT_AUTHORIZED")
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
                        checks["target_scope"] = Check.ESCALATE
                        reasons.append("TARGET_AMBIGUOUS")
                    else:
                        reasons.append("TARGET_NOT_AUTHORIZED")

            lineage_ok, lineage_reasons = self.validate_token_lineage(token)
            if token.parent_authority_ref:
                checks["delegation_chain"] = Check.PASS if lineage_ok else Check.FAIL
            reasons.extend(lineage_reasons)

        denial_key: Optional[tuple[str, str, Optional[str]]] = None
        if checks["trusted_correlation"] == Check.PASS and intent_ref is not None:
            denial_key = (proposal.subject, intent_ref, proposal.authority_ref)
            if denial_key in self._denied_intents:
                checks["route_substitution"] = Check.FAIL
                reasons.append("SUBSTITUTION_AFTER_DENIAL")

        reason_codes = tuple(dict.fromkeys(reasons))
        if not reason_codes and all(
            value in {Check.PASS, Check.NOT_APPLICABLE} for value in checks.values()
        ):
            decision = Decision.ALLOW
        elif any(value == Check.FAIL for value in checks.values()):
            # A hard failure always dominates an escalation request.
            decision = Decision.DENY
        elif any(value == Check.ESCALATE for value in checks.values()):
            decision = Decision.ESCALATE
        else:
            decision = Decision.DENY

        # Escalation is not denial. A clarified proposal may be reevaluated under the
        # same authority grant; only a hard denial creates sticky substitution state.
        if decision == Decision.DENY and denial_key is not None:
            self._denied_intents.add(denial_key)

        audit_id = self._next_id("AUD")
        previous_hash = self._audit[-1].event_hash if self._audit else "GENESIS"
        audit_checks = {key: value.value for key, value in checks.items()}
        event_hash = self._hash_audit_payload(
            audit_id,
            now,
            proposal.id,
            proposal.subject,
            decision,
            reason_codes,
            proposal.authority_ref,
            intent_ref,
            audit_checks,
            previous_hash,
        )
        audit = AuditEvent(
            id=audit_id,
            timestamp=now,
            proposal_ref=proposal.id,
            subject=proposal.subject,
            decision=decision,
            reason_codes=reason_codes,
            authority_ref=proposal.authority_ref,
            intent_ref=intent_ref,
            checks=audit_checks,
            previous_event_hash=previous_hash,
            event_hash=event_hash,
        )
        self._audit.append(audit)

        return GatewayDecision(
            id=self._next_id("GWD"),
            timestamp=now,
            proposal_ref=proposal.id,
            subject=proposal.subject,
            authority_ref=proposal.authority_ref,
            target_scope_ref=proposal.target_scope_ref,
            intent_ref=intent_ref,
            checks=checks,
            decision=decision,
            reason_codes=reason_codes,
            audit_event=audit,
        )
