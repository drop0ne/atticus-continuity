# CP-2026-08-26 — PAC deterministic text extraction and chapter index

```yaml
checkpoint_id: CP-2026-08-26-pac-text-extraction-index
timestamp: 2026-08-26
active_task: Advance P0 PAC source preservation using the locally recovered definitive First Edition TAR.
status: PARTIAL_COMPLETE_FULL_TEXT_MIRROR_PENDING
active_context_bundles:
  - CORE
  - PAC_GOVERNANCE
source:
  filename: PAC_FIRST_EDITION_DEFINITIVE(20260823-114607).tar
  size_bytes: 931840
  sha256: 2198f146bc56fe97d754a4e87bf1ecd9c3f03050b1ace2b215b5169c62b9a9a8
work_completed:
  - Built deterministic inert DOCX/SVG text extractor.
  - Extracted text projections locally from all 23 DOCX members and the SVG member without editorial rewriting.
  - Included document.xml plus present header/footer/footnotes/endnotes/comments WordprocessingML parts.
  - Preserved the SVG source verbatim as UTF-8 in the local projection set.
  - Ran extraction twice against the same TAR; output trees were byte-identical.
  - Built stable chapter/source index shards mapped to definitive member SHA-256 values and extracted-text SHA-256 values.
  - Preserved Heading-style structure separately from numbered-label observations so source irregularities are not silently repaired.
verification:
  deterministic_repeat_runs: 2
  deterministic_tree_digest_sha256: a2cb235fb5a1ab5da3e89a40e85a25e861f061b82609151fbe46ec61d41a1715
  total_projection_tree_bytes: 644507
  extracted_text_characters_observed: 512364
  explicitly_styled_headings_observed: 229
  chapter_index_part_1_sha256: a9f8bbb41d5a75cab03f63d9ac8705af063c68cac678bf5c3bfcf52ab86bc5c5
  chapter_index_part_2_sha256: 66bf677fc902546ba6fff5db364b59cf71569a63e49a70b728aa126f75cc9f3d
source_structure_observations:
  - Volume I labels I.2, I.8, I.11, I.12, and I.13 occur without corresponding Heading-style paragraphs.
  - Volume IV labels IV.41 through IV.60 occur without Heading-style paragraphs.
  - These observations do not establish that content is missing; no repair or inferred structure was applied.
files_added:
  - reference/source_integrity/extract_pac_text.py
  - migration/source-artifacts/pac/README.md
  - migration/source-artifacts/pac/PAC_TEXT_EXTRACTION-20260826.yaml
  - migration/source-artifacts/pac/PAC_FIRST_EDITION_DEFINITIVE-20260823.chapter-index.part1.yaml
  - migration/source-artifacts/pac/PAC_FIRST_EDITION_DEFINITIVE-20260823.chapter-index.part2.yaml
blocked_or_failed:
  - Current GitHub connector still does not expose the local TAR or generated projection directory as direct binary/file parameters.
  - Full per-member UTF-8 projection files therefore remain local in this checkpoint.
  - Exact raw TAR repository mirroring remains pending binary-capable transport.
open_questions:
  - ATTICUS v6.5.0-ABG raw duplicate bytes remain unavailable for SHA-256 comparison.
  - Exact historical PAC .tar.gz wrapper remains a lineage-only unknown.
next_actions:
  - Mirror full PAC UTF-8 projection set through a reliable file/binary transport and verify hashes.
  - Mirror exact PAC TAR bytes when a binary-capable transport is available and verify repository-retrieved SHA-256.
  - Retry ATTICUS raw-byte acquisition and immediately use REF-SRC-INT-0001 when available.
  - If source-byte access remains blocked, continue provider portability or independent replication work without weakening P0 standards.
```

The major advance is that PAC is now source-addressable below the volume level from the exact recovered member set, with reproducible extraction behavior and explicit structure anomalies preserved rather than normalized.
