# ADR-0008 — Canonical AMAS Component Binding

**Status:** ACCEPTED  
**Date:** 2026-08-14

## Context

ATTICUS v6.5.0-ABG is the controlling canonical ATTICUS release. The separate private repository `drop0ne/amas-spec` now contains a substantially hardened Authority Mapping and Arbitration System covering contextual authority, immutable memory-cell handling, deterministic conflict resolution, and an external Agent Authority Boundary.

The user explicitly designated this AMAS upgrade for integration into the local ATTICUS system and requested that it become canonical.

At designation time the live `amas-spec` default branch resolved to commit:

`c997fa75981e3ccfe921ef7fbd6d3cae46913425`

The relevant component identifiers at that revision are:

- AMAS Core `2.0-draft`, revision `2026-08-12`;
- AAB `0.4.1-draft`;
- AMCS reference engine `0.3.3`;
- AMCS protocol `v1.2.1 INTERNAL`.

## Decision

Integrate the AMAS revision above as a canonical component binding under ATTICUS v6.5.0-ABG.

Do **not** mint a new ATTICUS semantic version solely for this component integration. The parent canonical release remains `v6.5.0-ABG` until the user explicitly designates a successor release.

Record the binding in:

`atticus/canonical/AMAS_v2.0_CANONICAL_BINDING.md`

and require that record in normal continuity bootstrap and CORE hydration.

## Pinning rule

The canonical dependency is the immutable commit, not the moving `main` branch.

Therefore:

```text
newer upstream commit != automatic ATTICUS upgrade
repository reachability != authority
repository persistence != canonicalization
```

A later AMAS update requires explicit user designation and a new recorded revision.

## Governance effect

The binding imports the AMAS authority and memory constraints into canonical ATTICUS operation, including:

- data is not instruction;
- inference is not fact or delegation;
- reachability is not authorization;
- capability is not authority;
- successful execution does not widen authority;
- authorization is not proof of completion;
- deterministic conflict arbitration;
- read-only hydration by default;
- provenance-required supersession;
- an externalized side-effect authority boundary;
- bounded AMCS epistemic derivation.

Where ATTICUS/PAC or platform/system requirements impose stricter limits, the stricter controlling requirement remains in force.

## Verification boundary

The AMAS source remains a research draft and does not establish a production-containment certification claim.

Canonicalization means that these governance rules and the pinned specification revision are controlling ATTICUS component state. It does not convert reference implementations into automatically trusted execution code.

## Consequences

### Positive

- removes ambiguity over the AMAS version ATTICUS should use;
- makes the integration recoverable across sessions and models;
- prevents silent dependency drift;
- strengthens the explicit separation of data, model belief, authority, and execution;
- aligns continuity hydration with deterministic provenance and fail-closed behavior.

### Costs

- future AMAS upgrades require an explicit repin;
- the continuity repository now depends on an external private repository for deep AMAS implementation detail;
- production deployment still requires separate implementation, security, and verification work.