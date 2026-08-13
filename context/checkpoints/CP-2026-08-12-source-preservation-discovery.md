# CP-2026-08-12 — Source Preservation Discovery

```yaml
checkpoint_id: CP-2026-08-12-source-preservation-discovery
timestamp: 2026-08-12T19:54:58-05:00
active_task: Advance P0 preservation of complete PAC and ATTICUS source material.
status: ACTIVE
active_context_bundles:
  - CORE
decisions:
  - PAC Volumes V-X are no longer classified as existence-unknown; a primary session memory record documents them as members of a named definitive First Edition archive.
  - Exact PAC definitive archive bytes remain required before migration can be called complete.
  - The recorded PAC Canon Hash is preserved as evidence but its object/scope is unresolved and must not be mislabeled as the archive hash.
  - ATTICUS v6.5.0-ABG has two DOCX and two Markdown Library candidates with strongly matching sampled text; byte identity remains unverified.
  - Sampled-text equivalence is evidence, not a substitute for SHA-256 and complete diff verification.
files_changed:
  - migration/source-ledgers/PAC-FIRST-EDITION-DEFINITIVE-discovery.md
  - migration/source-ledgers/ATTICUS-v6.5.0-ABG-source-discovery.md
  - migration/SOURCE_INVENTORY.md
  - ROADMAP.md
evidence_added:
  - PAC_SESSION_MEMORY_CELL.txt identifies PAC_FIRST_EDITION_DEFINITIVE.tar.gz as an approximately 832K, 24-file definitive First Edition archive.
  - The PAC session record enumerates front matter, Volume 0, Volumes I-X, Amendment Addendum, Appendices A-F, glossary, and two architecture-diagram artifacts.
  - The PAC session record documents dedicated expansions for Volumes V-X and the selected Branch-A volume structure.
  - The PAC session record states standalone Volume V was not in the original uploads and was reconstructed from Volume III and prior-session references before later expansion.
  - Two ATTICUS DOCX and two ATTICUS Markdown Library artifacts under the v6.5.0-ABG full-stack filename were located.
  - Sampled sections across the ATTICUS duplicates match on release identity, canonical state, AMAS rules, conformance, migration, activation contract, and known limits.
experiments_changed: []
resolved_questions:
  - PAC Volumes V-X existed as documented components of the definitive First Edition source package.
open_questions:
  - Where are the exact bytes for PAC_FIRST_EDITION_DEFINITIVE.tar.gz or its 24 members?
  - What exact object does the PAC memory cell's recorded SHA-256 hash cover?
  - Are the duplicate ATTICUS DOCX/Markdown candidates byte-identical or merely text-equivalent?
  - Does the repository canonical ATTICUS file exactly reproduce the selected Library Markdown source?
blocking_unknowns:
  - Exact PAC definitive archive bytes not located in searchable Library.
  - Exact hashes for PAC standalone and ATTICUS duplicate candidates not yet computed.
  - Full Library-to-repository ATTICUS diff not yet executed.
next_actions:
  - Recover/materialize exact ATTICUS Markdown bytes and compute hashes.
  - Diff selected ATTICUS Library Markdown against atticus/canonical/ATTICUS_v6.5.0-ABG_CANONICAL.md.
  - Search local/user-controlled storage for PAC_FIRST_EDITION_DEFINITIVE.tar.gz and close filename variants.
  - Once PAC archive is recovered, hash archive and all members before extraction.
  - Preserve complete exact PAC and ATTICUS source representations and then build stable module/chapter indexes.
```

## Handoff

The highest-value source-preservation uncertainty changed during this cycle. PAC V-X existence is now supported by a primary session provenance artifact; the remaining PAC blocker is **exact source-byte recovery**, not whether the later volumes existed.

ATTICUS source discovery is also stronger: the Library contains both Markdown and DOCX full-stack candidates, with matching sampled content. Do not collapse these duplicates or declare the repository source complete until hashes and a full diff are available.
