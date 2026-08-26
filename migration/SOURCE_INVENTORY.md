# Source Migration Inventory

**Status:** ACTIVE / INCOMPLETE  
**Purpose:** track source artifacts that must be preserved before summaries or derived bundles are treated as complete.

## Power Avoidance Canon

### Definitive First Edition recovered

On 2026-08-23 the operator supplied `PAC_FIRST_EDITION_DEFINITIVE(20260823-114607).tar` as PAC and explicitly authorized repository mirroring.

Direct verification established:

```text
format: POSIX TAR
size_bytes: 931840
sha256: 2198f146bc56fe97d754a4e87bf1ecd9c3f03050b1ace2b215b5169c62b9a9a8
member_count: 24
```

Detailed ledger: `migration/source-ledgers/PAC-FIRST-EDITION-DEFINITIVE-discovery.md`  
Machine-readable member manifest: `migration/source-artifacts/pac/PAC_FIRST_EDITION_DEFINITIVE-20260823.manifest.yaml`

| Work | Discovery status | Migration status |
|---|---|---|
| Power Avoidance Canon — Volume 0 | RECOVERED_IN_DEFINITIVE_TAR | HASHED_LOCAL / RAW_REPOSITORY_BLOB_PENDING |
| Power Avoidance Canon — Volume I | RECOVERED_IN_DEFINITIVE_TAR | HASHED_LOCAL / RAW_REPOSITORY_BLOB_PENDING |
| Power Avoidance Canon — Volume II | RECOVERED_IN_DEFINITIVE_TAR | HASHED_LOCAL / RAW_REPOSITORY_BLOB_PENDING |
| Power Avoidance Canon — Volume III | RECOVERED_IN_DEFINITIVE_TAR | HASHED_LOCAL / RAW_REPOSITORY_BLOB_PENDING |
| Power Avoidance Canon — Volume IV | RECOVERED_IN_DEFINITIVE_TAR | HASHED_LOCAL / RAW_REPOSITORY_BLOB_PENDING |
| Power Avoidance Canon — Volume V | RECOVERED_IN_DEFINITIVE_TAR | HASHED_LOCAL / RAW_REPOSITORY_BLOB_PENDING |
| Power Avoidance Canon — Volume VI | RECOVERED_IN_DEFINITIVE_TAR | HASHED_LOCAL / RAW_REPOSITORY_BLOB_PENDING |
| Power Avoidance Canon — Volume VII | RECOVERED_IN_DEFINITIVE_TAR | HASHED_LOCAL / RAW_REPOSITORY_BLOB_PENDING |
| Power Avoidance Canon — Volume VIII | RECOVERED_IN_DEFINITIVE_TAR | HASHED_LOCAL / RAW_REPOSITORY_BLOB_PENDING |
| Power Avoidance Canon — Volume IX | RECOVERED_IN_DEFINITIVE_TAR | HASHED_LOCAL / RAW_REPOSITORY_BLOB_PENDING |
| Power Avoidance Canon — Volume X | RECOVERED_IN_DEFINITIVE_TAR | HASHED_LOCAL / RAW_REPOSITORY_BLOB_PENDING |
| Front matter / Amendment Addendum | RECOVERED_IN_DEFINITIVE_TAR | HASHED_LOCAL / RAW_REPOSITORY_BLOB_PENDING |
| Appendices A–F | RECOVERED_IN_DEFINITIVE_TAR | HASHED_LOCAL / RAW_REPOSITORY_BLOB_PENDING |
| Glossary / architecture artifacts | RECOVERED_IN_DEFINITIVE_TAR | HASHED_LOCAL / RAW_REPOSITORY_BLOB_PENDING |
| Supplied definitive TAR payload | RECOVERED_AND_HASHED | REPOSITORY_HASH_MANIFEST_MIRRORED / RAW_BLOB_PENDING |
| Historical `PAC_FIRST_EDITION_DEFINITIVE.tar.gz` wrapper | NAMED_BY_PRIMARY_SESSION_RECORD | EXACT_GZIP_WRAPPER_BYTES_NOT_VERIFIED |

The recovered 24-member set matches the historical logical manifest. Appendix F is physically named `RED_TEAM_ASSESSMENT_PAC.docx` in the recovered TAR.

The prior provenance record's `Canon Hash` value `96b9c30b...5756b8b7` does not equal the recovered TAR SHA-256. Its hashed object remains unknown.

Standalone pre-definitive PAC candidates remain useful for lineage and duplicate comparison, but they no longer control selection of the definitive member set after the operator supplied the definitive TAR.

### Deterministic source-text projection and chapter index

On 2026-08-26 the recovered definitive TAR was processed locally with an inert deterministic extractor. All 23 DOCX members and the SVG member were projected to UTF-8 without editorial rewriting. The DOCX projection reads text-bearing WordprocessingML parts in XML order; formatting/layout is not preserved and no macros, external links, or embedded content are executed.

Repository records:

```text
migration/source-artifacts/pac/PAC_TEXT_EXTRACTION-20260826.yaml
migration/source-artifacts/pac/PAC_FIRST_EDITION_DEFINITIVE-20260823.chapter-index.part1.yaml
migration/source-artifacts/pac/PAC_FIRST_EDITION_DEFINITIVE-20260823.chapter-index.part2.yaml
reference/source_integrity/extract_pac_text.py
```

Verification:

```text
deterministic repeat runs: 2
projection tree digest SHA-256: a2cb235fb5a1ab5da3e89a40e85a25e861f061b82609151fbe46ec61d41a1715
total projection tree bytes: 644507
extracted text characters observed: 512364
explicitly styled headings observed: 229
```

The chapter index maps each logical PAC member to its definitive source SHA-256 and its derived text-projection SHA-256. It preserves Heading-style paragraphs separately from numbered-label observations. Labels without Heading style are recorded as source-structure observations and are not silently repaired or promoted to inferred chapters.

Status: `LOCAL_TEXT_EXTRACTION_VERIFIED / CHAPTER_INDEX_MIRRORED / FULL_TEXT_PROJECTION_MIRROR_PENDING`.

### Repository byte-mirror boundary

The exact TAR is locally available and hashed. The currently connected GitHub write surface does not expose a local-file binary upload path, so the repository currently mirrors the byte size, archive SHA-256, all member SHA-256 values, provenance, deterministic extraction metadata, and chapter index—not the raw TAR blob or complete per-member text projection set itself. Any later raw upload must hash to `2198f146bc56fe97d754a4e87bf1ecd9c3f03050b1ace2b215b5169c62b9a9a8` before being accepted as the exact mirror.

## ATTICUS

### Canonical source set located

Detailed ledger: `migration/source-ledgers/ATTICUS-v6.5.0-ABG-source-discovery.md`

Located candidate artifacts:

```text
ATTICUS_v6_5_0_ABG_FULL_STACK.docx
ATTICUS_v6_5_0_ABG_FULL_STACK.docx
ATTICUS_v6_5_0_ABG_FULL_STACK.md
ATTICUS_v6_5_0_ABG_FULL_STACK.md
```

The Library contains two DOCX and two Markdown candidates under the same filenames but different file IDs/upload dates. Sampled sections match across each pair and reproduce the same v6.5.0-ABG specification. Exact byte identity remains unknown until hashes are computed.

The discovered source describes and explicitly declares:

- ATTICUS v6.5.0-ABG;
- W-Stack rev5.0;
- W1–W7 active;
- bounded single-pass W7;
- ABG v1.0 fail-closed;
- Behavior Kernel v1.2-ABG;
- SAFEGUARD/OPSEC;
- AMAS v1.2 with ABG binding;
- SIFP v1.1 / ATFP / ATCS / ATMD;
- HCII / Link-Layer / AVM / CMHM / Context-OCCAM;
- Ethical/Legal layer;
- Q-Stack planning/orchestration;
- output/verification layer;
- activation contract;
- validation/conformance categories;
- known limitations and migration procedure;
- canonical state declaration superseding v6.4.2-CMHM as the active baseline.

Migration status: `SOURCE_TEXT_LOCATED / FULL_DIFF_NOT_YET_VERIFIED`.

The repository canonical representation must still be completely diffed against a selected Library Markdown source before the source migration is marked verified.

## ATTICUS / AMAS manuscript sources

Located related manuscript artifacts include:

```text
AMAS_Symbalics_ATTICUS_Reader_Edition_v2.4_Pass9A.docx
AMAS_Symbalics_ATTICUS_Reader_Edition_v2.5_Pass9B.docx
```

These are research/manuscript sources and must not silently override the explicit canonical ATTICUS full-stack specification.

## Historical reconstruction sources

Library records also contain ATTICUS historical extraction/hydration research and executive findings. These are valuable for lineage but include explicit uncertainty and contamination warnings, especially the historical `pac://` namespace collision with PROTOTYPE-ATTICUS-CORE.

Historical reconstruction therefore remains a separate migration track from current canonical runtime preservation.

## Migration procedure

For each source artifact:

1. materialize or otherwise obtain exact original bytes through authorized access;
2. calculate SHA-256;
3. preserve original filename and source metadata;
4. compare duplicate candidates where lineage still matters;
5. identify canonical edition only from evidence or explicit author/operator designation;
6. extract text without editorial rewriting;
7. split into stable-address chunks/chapters where useful;
8. preserve exact source-to-chunk mapping;
9. generate retrieval bundle/index metadata;
10. mark repository byte mirroring verified only after a repository retrieval hashes to the source artifact's recorded SHA-256.

## Completion rule

No summary, invariant extraction, runtime bundle, or memory cell is a substitute for preservation of the complete available source bytes. A hash manifest or text projection is an integrity/recovery aid, not a replacement for the raw artifact.
