# PAC First Edition Definitive — Source Discovery Ledger

**Status:** SOURCE_IDENTITY_DOCUMENTED / DEFINITIVE_ARCHIVE_BYTES_NOT_YET_LOCATED  
**Evidence class:** user-controlled Library artifact + later internal manuscript references  
**Do not treat this ledger as a substitute for the original archive.**

## Primary discovered record

Library artifact:

```text
PAC_SESSION_MEMORY_CELL.txt
file_id: file_00000000524871fdaf7f4d25ab4aa2e4
created: 2026-03-14T00:43:59Z
```

The record identifies itself as an ATTICUS HCII session memory cell for a 2026-03-13 session whose objective was to produce the complete publication-ready First Edition of the Power Avoidance Canon.

It records:

```text
Archive: PAC_FIRST_EDITION_DEFINITIVE.tar.gz
Approximate archive size: 832K
File count: 24
```

The archive itself was not returned by the current Library searches. Its existence is therefore **documented by a provenance artifact**, while the exact archive bytes remain `NOT_YET_LOCATED`.

## Definitive manifest recorded by the memory cell

### Front matter

1. Author's Preface
2. How to Read This Book
3. Introduction
4. Volume 0 — Orientation

### Canonical volumes

5. Volume I — Foundations
6. Volume II — Psychology and Moral Failure
7. Volume III — Systems Design
8. Volume IV — Law and Institutions
9. Volume V — AI Architecture
10. Volume VI — Everyday Amplification
11. Volume VII — Failure Library
12. Volume VIII — Operational Discipline
13. Volume IX — Synthesis
14. Volume X — Termination

### Governance layer

15. Amendment Addendum

### Appendices

16. Appendix A — Operationalizing Contestability
17. Appendix B — Policy Applications
18. Appendix C — Intellectual Lineage
19. Appendix D — Criticisms and Responses
20. Appendix E — Worked Institutional Cases
21. Appendix F — Red Team Assessment

### Back matter

22. Glossary of Canon Terms

### Supplementary artifacts

23. Architecture Diagram (SVG)
24. Architecture Diagram (DOCX companion)

The memory cell estimates the total corpus at approximately 490K+ characters.

## Volume V–X evidence

The memory cell records a dedicated expansion phase for Volumes V–X:

- Volume V — AI Architecture: approximately 27,958 characters, 14 chapters.
- Volume VI — Everyday Amplification: approximately 17,184 characters, 11 chapters.
- Volume VII — Failure Library: approximately 15,593 characters, 11 chapters.
- Volume VIII — Operational Discipline: approximately 13,280 characters, 11 chapters.
- Volume IX — Synthesis: approximately 13,783 characters, 11 chapters.
- Volume X — Termination: approximately 9,840 characters, 9 chapters.

This is materially stronger than the previous `NOT_YET_LOCATED` state: Volumes V–X are now **documented components of a named definitive First Edition archive**. However, their exact standalone files or the definitive archive bytes have not yet been located in the searchable Library.

## Important provenance caveat for Volume V

The memory cell states that standalone Volume V was not among the original uploads used at the start of the session and that Volume V was reconstructed from a Volume III walkthrough plus prior session references before later expansion.

Therefore:

```text
existence_in_definitive_first_edition: SUPPORTED_BY_PRIMARY_SESSION_RECORD
standalone_pre-session_volume_v_source: NOT_ESTABLISHED
exact_definitive_volume_v_bytes: NOT_YET_LOCATED
```

This distinction must remain visible in lineage work.

## Fork resolution evidence

The record documents two competing later-volume structures and states that the operator uploaded a canonical 12-file set resolving the fork to the branch in which:

```text
VI = Everyday Amplification
VII = Failure Library
VIII = Operational Discipline
IX = Synthesis
X = Termination
```

This is evidence of an operator-controlled fork decision in that session. It does not independently prove the byte identity of the final archive.

## Hash evidence

The memory cell contains:

```text
Canon Hash: SHA-256:96b9c30b092d0a0adb34c8d0252a1100629569f85161f9e649bef4ce5756b8b7
```

**Hash scope is unresolved.** The record does not establish whether this value hashes the final TAR archive, a canonical text aggregation, a prior hydration package, or another object. Do not label it as the definitive archive hash until its scope is independently verified.

## Corroborating internal references

Later user-controlled manuscript records describe their P1 source lineage as "Power Avoidance Canon, First Edition Definitive: Volumes 0-X, appendices, red-team assessment, architecture diagram, and memory-cell records." These references corroborate that the definitive First Edition existed as an internal source package, but remain secondary to the original archive bytes.

## Migration classification

| Object | Discovery status | Migration status |
|---|---|---|
| PAC First Edition definitive identity | DOCUMENTED | LEDGER_CREATED |
| PAC Volumes V-X existence in definitive edition | SUPPORTED | MANIFEST_ONLY |
| `PAC_FIRST_EDITION_DEFINITIVE.tar.gz` exact bytes | NOT_YET_LOCATED | BLOCKED_PENDING_SOURCE_BYTES |
| Archive SHA-256 | UNKNOWN | BLOCKED_PENDING_BYTES |
| Scope of recorded `96b9...` hash | UNKNOWN | REQUIRES_VERIFICATION |

## Next verification steps

1. Search local/user-controlled storage for `PAC_FIRST_EDITION_DEFINITIVE.tar.gz` and close filename variants.
2. If located, preserve the original bytes before extraction.
3. Calculate SHA-256 of the archive and all 24 members.
4. Compare the archive manifest against this session-memory manifest.
5. Extract UTF-8 source representations without editorial rewriting.
6. Assign stable IDs to front matter, Volumes 0-X, appendices, glossary, and supplementary artifacts.
7. Preserve the session memory cell itself as lineage evidence, but never promote it above the exact archive once the archive is recovered.

## Authority rule

This ledger updates **discovery status only**. It does not independently redesign, amend, or canonicalize PAC content.
