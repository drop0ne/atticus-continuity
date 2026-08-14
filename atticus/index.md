# ATTICUS Index

This index makes the canonical ATTICUS framework addressable without treating a summary as a replacement for the full source.

## Current canonical release

- Canonical state record: `canonical/ATTICUS_v6.5.0-ABG_CANONICAL.md`
- Stable source/module map: `source/ATTICUS_v6.5.0-ABG-source-map.yaml`
- Full source migration ledger: `../migration/source-ledgers/ATTICUS-v6.5.0-ABG-source-discovery.md`

## Source status

The complete v6.5.0-ABG specification has been located in the user-controlled Library as two Markdown and two DOCX candidates. Sampled sections strongly support textual equivalence, but exact byte identity and a full Library-to-repository diff remain unresolved.

Therefore:

```text
located source text != verified byte-identical archive
canonical summary != complete source preservation
sampled equivalence != complete diff
```

## Stable section IDs

`ATTICUS-S01` through `ATTICUS-S31` map directly to the 31 documented sections of the v6.5.0-ABG full-stack specification. The source map is the machine-readable registry.

These IDs are retrieval addresses. They do not rewrite, reorder, or silently canonicalize the underlying source.

## Retrieval rule

For ordinary continuity, load the compact canonical state and `CORE` bundle.

For framework-level work, load `context/bundles/ATTICUS-RUNTIME.yaml` plus the source map. Retrieve the relevant full source section only when the task depends on exact wording or implementation detail.

For historical questions, use historical lineage records separately; older versions must not be allowed to silently override v6.5.0-ABG.

## Verification boundary

Do not mark ATTICUS source migration complete until:

1. exact source bytes are materialized;
2. SHA-256 hashes are recorded;
3. duplicate Markdown candidates are completely diffed;
4. DOCX package/text differences are classified;
5. the selected Markdown source is completely diffed against the repository representation;
6. any omissions or semantic deltas are explicitly reconciled.
