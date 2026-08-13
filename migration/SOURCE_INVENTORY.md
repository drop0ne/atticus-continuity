# Source Migration Inventory

**Status:** ACTIVE / INCOMPLETE  
**Purpose:** track source artifacts that must be preserved before summaries or derived bundles are treated as complete.

## Power Avoidance Canon

Current Library discovery now supports two distinct source layers:

1. directly located standalone source artifacts for Volumes I–IV; and
2. a provenance memory cell documenting a named definitive First Edition archive containing Volumes 0–X plus appendices and supplementary files.

Detailed ledger: `migration/source-ledgers/PAC-FIRST-EDITION-DEFINITIVE-discovery.md`

| Work | Discovery status | Migration status |
|---|---|---|
| Power Avoidance Canon — Volume I | LOCATED_STANDALONE | NOT_YET_MIGRATED_FULL_TEXT |
| Power Avoidance Canon — Volume II | LOCATED_STANDALONE | NOT_YET_MIGRATED_FULL_TEXT |
| Power Avoidance Canon — Volume III | LOCATED_STANDALONE | NOT_YET_MIGRATED_FULL_TEXT |
| Power Avoidance Canon — Volume IV | LOCATED_STANDALONE | NOT_YET_MIGRATED_FULL_TEXT |
| Power Avoidance Canon — Volume V | DOCUMENTED_IN_DEFINITIVE_MANIFEST | EXACT_DEFINITIVE_BYTES_NOT_YET_LOCATED |
| Power Avoidance Canon — Volume VI | DOCUMENTED_IN_DEFINITIVE_MANIFEST | EXACT_DEFINITIVE_BYTES_NOT_YET_LOCATED |
| Power Avoidance Canon — Volume VII | DOCUMENTED_IN_DEFINITIVE_MANIFEST | EXACT_DEFINITIVE_BYTES_NOT_YET_LOCATED |
| Power Avoidance Canon — Volume VIII | DOCUMENTED_IN_DEFINITIVE_MANIFEST | EXACT_DEFINITIVE_BYTES_NOT_YET_LOCATED |
| Power Avoidance Canon — Volume IX | DOCUMENTED_IN_DEFINITIVE_MANIFEST | EXACT_DEFINITIVE_BYTES_NOT_YET_LOCATED |
| Power Avoidance Canon — Volume X | DOCUMENTED_IN_DEFINITIVE_MANIFEST | EXACT_DEFINITIVE_BYTES_NOT_YET_LOCATED |
| `PAC_FIRST_EDITION_DEFINITIVE.tar.gz` | NAMED_BY_PRIMARY_SESSION_RECORD | ARCHIVE_BYTES_NOT_YET_LOCATED |

The previous `NOT_YET_LOCATED` state for Volumes V–X is therefore retired. Their existence as components of the definitive First Edition is supported by the user-controlled `PAC_SESSION_MEMORY_CELL.txt`, which records the complete 24-file archive manifest and a dedicated V–X expansion phase. This does **not** mean the exact definitive source bytes have been recovered.

The memory cell also records that standalone Volume V was not in the original session uploads and was reconstructed from a Volume III walkthrough plus prior-session references before expansion. That provenance distinction must remain visible.

### Located standalone filenames for Volumes I–IV

Observed candidate source filenames include:

```text
THE POWER AVOIDANCE CANON Vol I.docx
THE POWER AVOIDANCE CANON Vol I.odt
THE POWER AVOIDANCE CANON Vol I(1).odt
THE POWER AVOIDANCE CANON Vol II.odt
THE POWER AVOIDANCE CANON Vol II(1).odt
THE POWER AVOIDANCE CANON Vol III.docx
THE POWER AVOIDANCE CANON Vol III.odt
THE POWER AVOIDANCE CANON Vol IV.docx
THE POWER AVOIDANCE CANON Vol IV.odt
THE POWER AVOIDANCE CANON Vol IV(1).odt
```

Duplicate-looking filenames require exact byte hashes, document metadata, and textual comparison before any edition is collapsed into a single source identity.

### Definitive First Edition evidence

The discovered memory cell names:

```text
PAC_FIRST_EDITION_DEFINITIVE.tar.gz
approximate size: 832K
file count: 24
```

Its manifest includes front matter, Volume 0, Volumes I–X, an Amendment Addendum, Appendices A–F, a glossary, and architecture-diagram artifacts.

The same memory cell contains a `Canon Hash` value, but the object covered by that hash is not established. It must not be labeled as the archive hash until verified against recovered bytes.

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
4. compare duplicate candidates;
5. identify canonical edition only from evidence or explicit author designation;
6. extract text without editorial rewriting;
7. split into stable-address chunks/chapters where useful;
8. preserve exact source-to-chunk mapping;
9. generate retrieval bundle/index metadata;
10. mark migration verified only after completeness checks.

## Completion rule

No summary, invariant extraction, runtime bundle, or memory cell is a substitute for preservation of the complete available source bytes.
