# PAC First Edition Definitive — Source Recovery Ledger

**Status:** DEFINITIVE_MEMBER_SET_RECOVERED / TAR_PAYLOAD_HASHED / REPOSITORY_RAW_BLOB_PENDING_TRANSPORT  
**Evidence class:** user-designated source artifact + prior user-controlled provenance record  
**Controlling integrity record:** `migration/source-artifacts/pac/PAC_FIRST_EDITION_DEFINITIVE-20260823.manifest.yaml`

## 2026-08-23 recovery event

The operator supplied the archive:

```text
PAC_FIRST_EDITION_DEFINITIVE(20260823-114607).tar
```

and identified it as PAC, then explicitly instructed that the PAC TAR be encoded/mirrored into the continuity repository. The supplied file was inspected directly before any repository update.

Observed archive properties:

```text
format: POSIX TAR
size_bytes: 931840
sha256: 2198f146bc56fe97d754a4e87bf1ecd9c3f03050b1ace2b215b5169c62b9a9a8
regular_file_members: 24
```

All 24 members were individually hashed. All 23 DOCX members are structurally valid ZIP/Office packages and the SVG is valid XML. The complete member-level hashes, byte sizes, TAR ordering, and logical PAC ordering are recorded in the machine-readable manifest above.

## Match to the historical definitive manifest

The recovered member set maps to all 24 roles recorded by the earlier `PAC_SESSION_MEMORY_CELL.txt`:

1. Author's Preface
2. How to Read This Book
3. Introduction
4. Volume 0 — Orientation
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
15. Amendment Addendum
16. Appendix A — Operationalizing Contestability
17. Appendix B — Policy Applications
18. Appendix C — Intellectual Lineage
19. Appendix D — Criticisms and Responses
20. Appendix E — Worked Institutional Cases
21. Appendix F — Red Team Assessment
22. Glossary of Canon Terms
23. Architecture Diagram — SVG
24. Architecture Diagram — DOCX companion

The recovered physical filename for Appendix F is `RED_TEAM_ASSESSMENT_PAC.docx`; it is not prefixed `APPENDIX_`. This resolves the previous filename ambiguity without changing the logical Appendix F role recorded by the historical manifest.

## Historical wrapper distinction

The earlier provenance record named:

```text
PAC_FIRST_EDITION_DEFINITIVE.tar.gz
approximate size: 832K
file count: 24
```

The 2026-08-23 supplied artifact is an **uncompressed TAR**, not the historical gzip wrapper. Therefore:

```text
canonical 24-member source set: RECOVERED_AND_HASHED
supplied TAR payload bytes: RECOVERED_AND_HASHED
historical .tar.gz wrapper bytes: NOT_VERIFIED
```

Do not claim that the SHA-256 of the supplied TAR is the hash of the historical `.tar.gz` byte stream. Gzip framing, headers, timestamps, compression implementation, and compression level can change wrapper bytes while preserving the same TAR payload.

## Previously recorded Canon Hash

The historical memory cell contains:

```text
SHA-256:96b9c30b092d0a0adb34c8d0252a1100629569f85161f9e649bef4ce5756b8b7
```

That value does not equal the recovered TAR SHA-256. Its scope remains unresolved and must not be relabeled as an archive hash without identifying the exact object it covered.

## Volume V provenance caveat retained

The earlier session record states that standalone Volume V was not among the original session uploads and was reconstructed before the later definitive expansion. Recovery of the final definitive Volume V bytes does not erase that historical lineage distinction.

## Migration classification

| Object | Current status |
|---|---|
| PAC First Edition definitive identity | OPERATOR_DESIGNATED / SUPPORTED_BY_PRIOR_PROVENANCE |
| Complete logical 24-member First Edition set | RECOVERED_AND_HASHED |
| Volumes 0–X definitive member bytes | RECOVERED_AND_HASHED |
| Appendices A–F definitive member bytes | RECOVERED_AND_HASHED |
| Glossary and architecture artifacts | RECOVERED_AND_HASHED |
| Supplied uncompressed TAR payload | RECOVERED_AND_HASHED |
| Supplied TAR SHA-256 | `2198f146bc56fe97d754a4e87bf1ecd9c3f03050b1ace2b215b5169c62b9a9a8` |
| Exact historical gzip wrapper bytes | NOT_VERIFIED |
| Historical `96b9...` hash scope | UNRESOLVED |
| Raw TAR bytes inside GitHub | PENDING_BINARY_CAPABLE_TRANSPORT |
| Hash/member manifest inside GitHub | MIRRORED |

## Repository transport limitation

The current connected GitHub write surface can create text/Git blobs but does not expose the locally mounted TAR as a direct file parameter and does not expose a repository credential inside the execution container. The raw 931,840-byte TAR therefore cannot be defensibly uploaded byte-for-byte through this session without routing a megabyte-scale text encoding through the model.

The repository mirror now preserves the exact TAR hash, byte size, complete 24-member hash manifest, source designation, and recovery state. A later binary-capable transport must upload the exact local TAR and verify SHA-256 equality before the repository status becomes `REPOSITORY_MIRRORED_EXACT_BYTES`.

## Next source-preservation steps

1. Move the exact TAR through a binary-capable GitHub upload path and verify SHA-256 after retrieval.
2. Extract source text from the recovered definitive DOCX files without editorial rewriting.
3. Build a stable PAC volume/chapter index mapped back to member hashes.
4. Preserve the historical `.tar.gz` wrapper only if its exact bytes are later located; it is lineage evidence, not a reason to delay use of the recovered definitive member set.
5. Continue ATTICUS exact-byte preservation as the remaining P0 source-recovery problem.

## Authority rule

This recovery record mirrors operator-designated source state. It does not independently amend PAC content. The recovered source bytes control over earlier summaries or reconstruction notes for the same definitive edition.
