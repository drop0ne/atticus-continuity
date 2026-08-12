# Source Migration Inventory

**Status:** ACTIVE / INCOMPLETE  
**Purpose:** track source artifacts that must be preserved before summaries or derived bundles are treated as complete.

## Power Avoidance Canon

Current Library discovery located source artifacts for Volumes I–IV.

| Work | Discovery status | Migration status |
|---|---|---|
| Power Avoidance Canon — Volume I | LOCATED | NOT_YET_MIGRATED_FULL_TEXT |
| Power Avoidance Canon — Volume II | LOCATED | NOT_YET_MIGRATED_FULL_TEXT |
| Power Avoidance Canon — Volume III | LOCATED | NOT_YET_MIGRATED_FULL_TEXT |
| Power Avoidance Canon — Volume IV | LOCATED | NOT_YET_MIGRATED_FULL_TEXT |
| Power Avoidance Canon — Volume V | NOT_YET_LOCATED | BLOCKED_PENDING_SOURCE |
| Power Avoidance Canon — Volume VI | NOT_YET_LOCATED | BLOCKED_PENDING_SOURCE |
| Power Avoidance Canon — Volume VII | NOT_YET_LOCATED | BLOCKED_PENDING_SOURCE |
| Power Avoidance Canon — Volume VIII | NOT_YET_LOCATED | BLOCKED_PENDING_SOURCE |
| Power Avoidance Canon — Volume IX | NOT_YET_LOCATED | BLOCKED_PENDING_SOURCE |
| Power Avoidance Canon — Volume X | NOT_YET_LOCATED | BLOCKED_PENDING_SOURCE |

The current Volume I source describes the Canon as ten volumes. `NOT_YET_LOCATED` means only that the current discovery pass did not locate an exact source artifact. It must not be interpreted as proof that a volume does not exist.

### Located filenames

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

Duplicate-looking filenames require exact byte hashes, document metadata, and textual comparison before any edition is designated canonical.

## ATTICUS

### Canonical candidate located

```text
ATTICUS_v6_5_0_ABG_FULL_STACK.docx
ATTICUS_v6_5_0_ABG_FULL_STACK(1).docx
```

The discovered source describes:

- ATTICUS v6.5.0-ABG;
- W-Stack rev5.0;
- W1–W7;
- bounded single-pass W7;
- ABG v1.0;
- Behavior Kernel v1.2-ABG;
- SAFEGUARD/OPSEC;
- AMAS;
- SIFP / ATFP / ATCS / ATMD;
- HCII / Link-Layer / AVM / CMHM / Context-OCCAM;
- Ethical/Legal layer;
- Q-Stack planning/orchestration;
- output/verification layer;
- activation contract;
- known limitations and migration procedure.

Migration status: `NOT_YET_MIGRATED_FULL_TEXT`.

The two candidate files require hash and content comparison before being collapsed into one source identity.

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

No summary, invariant extraction, or runtime bundle is a substitute for preservation of the complete available source.
