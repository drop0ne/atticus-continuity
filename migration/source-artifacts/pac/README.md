# PAC source-text extraction status

The definitive PAC First Edition TAR is locally recovered and hashed. This directory tracks deterministic text projections and source-structure indexes derived from that exact TAR.

Controlling source TAR SHA-256:

`2198f146bc56fe97d754a4e87bf1ecd9c3f03050b1ace2b215b5169c62b9a9a8`

## Repository-tracked artifacts

- `PAC_FIRST_EDITION_DEFINITIVE-20260823.manifest.yaml` — original 24-member integrity manifest.
- `PAC_TEXT_EXTRACTION-20260826.yaml` — extraction provenance, reproducibility evidence, and transport boundary.
- `PAC_FIRST_EDITION_DEFINITIVE-20260823.chapter-index.part1.yaml` — logical members 1–12.
- `PAC_FIRST_EDITION_DEFINITIVE-20260823.chapter-index.part2.yaml` — logical members 13–24.
- `reference/source_integrity/extract_pac_text.py` — deterministic inert extractor.

## Extraction boundary

For DOCX members the extractor reads WordprocessingML text-bearing parts and emits paragraph text in XML order. It does not preserve layout or formatting and does not execute macros, external links, or embedded content. The SVG member is projected verbatim as UTF-8.

The text projections are derived recovery aids, **not substitutes for the original DOCX/TAR bytes**.

Two independent local runs against the same TAR produced the same aggregate projection-tree digest:

`a2cb235fb5a1ab5da3e89a40e85a25e861f061b82609151fbe46ec61d41a1715`

## Structure rule

The chapter indexes preserve observed Heading-style paragraphs and separately record numbered labels that do not carry a Heading style. The repository must not silently repair, renumber, or infer missing chapter structure from those differences.

## Remaining transport gap

The complete UTF-8 projection set and exact 931,840-byte TAR blob are not yet repository-mirrored through the current connector. Their hashes and extraction/index metadata are preserved so a later binary-capable transport can be verified before promotion to exact repository-mirrored state.
