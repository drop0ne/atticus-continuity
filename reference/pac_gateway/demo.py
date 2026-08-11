"""Small inert demonstration of PAC gateway decisions."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

from .pac_gateway import (
    ActionIntentBinding,
    ActionProposal,
    AuthorityToken,
    Gateway,
    TargetScope,
)


NOW = datetime(2026, 8, 11, 23, 0, tzinfo=timezone.utc)


def trusted_demo_intent(proposal: ActionProposal) -> ActionIntentBinding:
    return ActionIntentBinding(
        id=f"BIND-{proposal.id}",
        issuer="trusted-demo-orchestrator",
        proposal_ref=proposal.id,
        intent_ref=proposal.semantic_action_id,
        issued_at=NOW - timedelta(minutes=1),
        expires_at=NOW + timedelta(minutes=10),
        provenance="demo-correlation",
        authority_ref=proposal.authority_ref,
    )


def build_gateway() -> Gateway:
    authority = AuthorityToken(
        id="AUTH-DEMO-1",
        issuer="demo-authority",
        subject="agent-demo",
        issued_at=NOW - timedelta(minutes=5),
        expires_at=NOW + timedelta(minutes=30),
        objective_scope=frozenset({"inspect-sandbox"}),
        target_scope_refs=frozenset({"TGT-DEMO-1"}),
        capability_scope=frozenset({"read"}),
        resource_scope=frozenset({"simulated-dataset"}),
        provenance="demo-explicit-grant",
    )
    target = TargetScope(
        id="TGT-DEMO-1",
        identifiers=frozenset({"sim://demo/alpha"}),
        allowed_effects=frozenset({"observe"}),
        real_world_effects_allowed=False,
    )
    return Gateway(
        authority_tokens={authority.id: authority},
        target_scopes={target.id: target},
        intent_resolver=trusted_demo_intent,
        now=lambda: NOW,
    )


def make_proposal(
    proposal_id: str,
    *,
    authority_ref: str | None = "AUTH-DEMO-1",
    capability: str = "read",
    semantic_action_id: str = "inspect-alpha",
    uncertain_target: bool = False,
    peer_support_count: int = 0,
) -> ActionProposal:
    return ActionProposal(
        id=proposal_id,
        subject="agent-demo",
        objective="inspect-sandbox",
        target_scope_ref="TGT-DEMO-1",
        target_identifiers=frozenset({"sim://demo/alpha"}),
        capability=capability,
        resource="simulated-dataset",
        effect="observe",
        authority_ref=authority_ref,
        semantic_action_id=semantic_action_id,
        uncertain_target=uncertain_target,
        peer_support_count=peer_support_count,
    )


def main() -> None:
    gateway = build_gateway()
    scenarios = [
        make_proposal("P-DEMO-1"),
        make_proposal("P-DEMO-2", authority_ref=None),
        make_proposal("P-DEMO-3", authority_ref=None, peer_support_count=100),
        make_proposal("P-DEMO-4", uncertain_target=True, semantic_action_id="uncertain-alpha"),
        make_proposal("P-DEMO-5", capability="write", semantic_action_id="change-alpha"),
        make_proposal("P-DEMO-6", capability="read", semantic_action_id="change-alpha"),
    ]

    output = []
    for item in scenarios:
        decision = gateway.evaluate(item)
        output.append(
            {
                "proposal": item.id,
                "trusted_intent": decision.intent_ref,
                "decision": decision.decision.value,
                "reason_codes": list(decision.reason_codes),
                "audit_hash": decision.audit_event.event_hash,
            }
        )

    print(json.dumps(output, indent=2))
    print(f"audit_chain_valid={gateway.verify_audit_chain()}")


if __name__ == "__main__":
    main()
