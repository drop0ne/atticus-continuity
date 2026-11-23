# ATTICUS v6.5.0-ABG — Source Discovery Ledger

**Status:** MARKDOWN_BYTE_IDENTITY_VERIFIED_2026-11-22 / DOCX_ZIP_IDENTITY_UNRESOLVED

**2026-11-22 update:** Four accessible 42,375-byte Markdown copies returned identical SHA-256 `5c8dff836d50cb372c6dcb450727ad9fad0e6b7d2704902d3c0ee2652e4055ad`. One complete Markdown source is preserved at `atticus/source/ATTICUS_v6_5_0_ABG_FULL_STACK.md`. Older observations below are retained as historical August 2026 evidence.  
**Target:** preserve the complete provider-neutral canonical ATTICUS v6.5.0-ABG specification independently of platform memory.

## Located Library artifacts

Two DOCX candidates:

```text
ATTICUS_v6_5_0_ABG_FULL_STACK.docx
file_id: file_000000009294722fa0d76b7d749718a4
created: 2026-07-11T00:50:19Z

ATTICUS_v6_5_0_ABG_FULL_STACK.docx
file_id: file_000000002bd081f58b1db228ebd8c9bb
created: 2026-07-21T14:17:00Z
```

Two Markdown candidates:

```text
ATTICUS_v6_5_0_ABG_FULL_STACK.md
file_id: file_00000000090c722f951a76cd7058b15d
created: 2026-07-11T00:50:20Z

ATTICUS_v6_5_0_ABG_FULL_STACK.md
file_id: file_000000002ea0820c9ed1207992156b5b
created: 2026-07-21T14:17:00Z
```

## Textual identity evidence

Search and open-file inspection returned matching sampled passages across both DOCX copies and both Markdown copies, including:

- release identity and release date;
- canonical framework version `ATTICUS Framework v6.5.0-ABG`;
- `ATTICUS_ABG_W7_INTEGRATION_v1_0` patch identity;
- W-Stack rev5.0 and W7 v2.0 bounded single-pass default;
- ABG v1.0;
- Behavior Kernel v1.2-ABG;
- canonical layer stack;
- AMAS memory authority rules;
- validation/conformance categories;
- migration from v6.4.2-CMHM;
- current activation contract;
- known limits;
- canonical state declaration.

This provides strong evidence that the duplicate-looking Library artifacts carry the same specification text. It does **not** establish byte-for-byte identity because exact file hashes have not yet been computed.

## Canonical declaration recovered from source

The source explicitly declares:

```text
Current framework: ATTICUS v6.5.0-ABG
Current W-Stack: rev5.0
W1-W7: active
W7: bounded single-pass default
ABG: v1.0 active and fail-closed
Behavior Kernel: v1.2-ABG
SAFEGUARD/OPSEC: active and non-overridable
AMAS: v1.2 with ABG integration binding
SIFP: v1.1
ATFP/ATCS/ATMD: active
HCII/Context Hydration/Link-Layer: active
AVM: active
CMHM: v0.1 active
Q-Stack/Quantizer: active
Secretary Mode and Context-OCCAM: available on invocation
```

The source also explicitly states that this release supersedes the v6.4.2-CMHM W7-off baseline while retaining the earlier baseline as historical lineage.

## Source coverage

The Markdown artifact contains the full structured specification beginning with Release Identity and extending through at least the documented 31 sections. Open-file output was truncated by retrieval limits, not because the source was incomplete.

The current repository already contains `atticus/canonical/ATTICUS_v6.5.0-ABG_CANONICAL.md`, but preservation work must compare that repository representation against this Library source before declaring the migration complete.

## Migration classification

| Object | Discovery status | Migration status |
|---|---|---|
| v6.5.0-ABG full-stack specification | LOCATED | SOURCE_TEXT_AVAILABLE |
| DOCX duplicate relationship | STRONGLY_TEXT_EQUIVALENT | BYTE_IDENTITY_UNKNOWN |
| Markdown duplicate relationship | STRONGLY_TEXT_EQUIVALENT | BYTE_IDENTITY_UNKNOWN |
| Exact SHA-256 per candidate | UNKNOWN | BLOCKED_PENDING_SOURCE_BYTES |
| Repo canonical file completeness vs Library Markdown | NOT_YET_VERIFIED | REQUIRES_DIFF |

## Required next steps

1. Materialize or otherwise obtain exact bytes for all four candidate files.
2. Calculate SHA-256 and byte sizes.
3. Compare Markdown copies byte-for-byte and normalized-text-to-normalized-text.
4. Compare DOCX package bytes and extracted text.
5. Diff the selected Library Markdown against `atticus/canonical/ATTICUS_v6.5.0-ABG_CANONICAL.md`.
6. If any difference exists, classify each delta as formatting, extraction artifact, omission, or semantic change.
7. Only after the diff is clean or explicitly reconciled, mark the full canonical source migration `VERIFIED`.

## Non-claim

Matching sampled text does not prove that every byte or every hidden document property is identical. Until hashes and a complete diff exist, duplicate collapse remains provisional.

## November 22, 2026 synchronization verification

- Four Markdown sources: 42,375 bytes each, SHA-256 identical (`5c8dff836d50cb372c6dcb450727ad9fad0e6b7d2704902d3c0ee2652e4055ad`).
- Exact complete Markdown release source preserved in `atticus/source/ATTICUS_v6_5_0_ABG_FULL_STACK.md`.
- The canonical-state record and explicitly pinned August AMAS v2.0 component binding remain controlling; this historical July release text does not roll them back.
- Library project ZIPs discovered but raw bytes not accessible: `ATTICUS_v6.5.0-ABG_FULL_STACK.zip` (79,430 bytes) and `ATTICUS_GLOBAL_MEMORY_HANDOFF_v6.5.0-ABG.zip` (82,609 bytes).
- ZIP internal hashes and DOCX byte identity were not independently reverified in this synchronization.
- The compact P1 memory-seed file is a recovery reference, not evidence of a successful account-memory mutation.

Current migration status: `MARKDOWN_MIRRORED_AND_HASHED / ZIP_DOCX_PENDING`.
