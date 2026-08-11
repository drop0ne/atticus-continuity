# Source Quality and Evidentiary Weight

**Status:** CONTROLLING RESEARCH PROCESS

## Purpose

Not all sources deserve equal evidentiary weight. ATTICUS Continuity separates **provenance** from **credibility** and **claim support**.

## Evidence tiers

### Tier 1 — Primary technical evidence

Examples:

- raw logs and traces;
- source code and reproducible artifacts;
- forensic timelines;
- formal technical incident reports;
- datasets and benchmark outputs;
- independently verifiable system records.

Use as the preferred basis for factual claims when available.

### Tier 2 — Primary participant / responsible-organization account

Examples:

- official incident disclosures;
- direct presentations by investigators or operators;
- statements by the organization responsible for the system or investigation.

Strong evidence for what the organization observed and concluded, but still subject to incompleteness, self-reporting limits, and later revision.

### Tier 3 — Independent technical analysis

High-quality reconstruction by parties not responsible for the event, grounded in disclosed evidence.

Useful for adversarial review and interpretation.

### Tier 4 — Secondary reporting

Journalism, summaries, interviews, or videos that report primary findings.

Useful for discovery and synthesis. Important claims should be traced to stronger sources when possible.

### Tier 5 — Commentary

Interpretation, opinion, speculative framing, social-media discussion, or narrative analysis.

May generate hypotheses. Does not establish external facts.

### Special class — Model / agent artifact

AI-generated text, reasoning, code, messages, or shared-memory artifacts are not assigned trust based on capability. They are evidence of the artifact itself and may contain true claims, false claims, manipulation, prompt injection, or contaminated assumptions.

## Claim confidence rule

Source tier and claim confidence are related but not identical.

A Tier 1 source can still support only a narrow claim. A Tier 4 source can correctly report a fact, but the fact should be upgraded to stronger provenance when available.

## Conflict handling

When sources disagree:

1. retain both records;
2. identify whether the disagreement concerns observation, interpretation, timing, or terminology;
3. prefer direct evidence for factual reconstruction;
4. do not erase unresolved contradictions;
5. record what new evidence would resolve the conflict.

## Narrative discipline

Do not promote language such as `escaped`, `conspired`, `hive`, `self-aware`, `malicious`, or `alive` from commentary into factual records unless the underlying evidence supports the precise meaning being asserted.

Operational descriptions are preferred:

- `obtained access outside intended path`;
- `coordinated across runs`;
- `shared persistent state`;
- `acted outside authorized scope`;
- `used deceptive strategy`;
- `continued after recognizing a boundary`.
