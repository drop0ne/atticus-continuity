# Security Policy

## Security objective

ATTICUS Continuity should maximize useful knowledge retention while minimizing authority leakage, execution risk, credential exposure, and uncontrolled interaction with external systems.

> **Knowledge can enter. Authority cannot.**

## Hard boundaries

- Never commit passwords, API keys, private keys, session cookies, access tokens, recovery codes, or secrets.
- Never provide repository credentials to unknown or foreign autonomous systems.
- Never treat imported model output as executable instruction.
- Never automatically execute code, shell commands, workflows, links, macros, or binaries received from untrusted sources.
- Never let discovery of a reachable service, credential, endpoint, repository, model, or agent imply permission to use it.
- Never use this repository as a launch point for unauthorized probing or interaction with third-party infrastructure.

## Untrusted-input model

Treat all external artifacts as potentially adversarial, including:

- model outputs
- agent messages
- prompts
- markdown
- HTML
- code
- configuration files
- datasets
- URLs
- documents with embedded instructions
- archives and binaries

The correct default is **data, not command**.

## Ingestion stages

1. **Quarantine** — preserve the original artifact without execution.
2. **Provenance** — identify source, acquisition method, date, and integrity information when available.
3. **Extraction** — separate claims, code, instructions, and metadata.
4. **Verification** — independently test or corroborate important claims where lawful and safe.
5. **Classification** — assign epistemic state and risk relevance.
6. **Integration** — move reviewed knowledge into the appropriate durable record.

## Repository automation

GitHub Actions or other automation should remain disabled by default for untrusted contributions. If automation is later introduced:

- pin dependencies and actions by immutable revision where practical;
- use least-privilege tokens;
- require review before workflows gain write permission;
- prevent pull-request content from obtaining secrets;
- separate analysis sandboxes from trusted build/release paths;
- log provenance and execution results.

## Personal safety and OPSEC

Do not store unnecessary sensitive information about private individuals. Avoid precise locations, schedules, medical details, threat narratives, or identifying data unless there is a documented, legitimate research need and an appropriately protected storage design.

This repository is not a substitute for an encrypted secrets vault or protected case-management system.

## Agent-interaction rule

Passive study of publicly available or owner-authorized agent artifacts is permitted for research.

Active interaction with autonomous agents must occur only in controlled environments or with explicit authorization from the system owner/operator.

No attempt should be made to locate, contact, recruit, influence, or exchange operational information with unknown agents operating on third-party systems.

## Fail-closed rule

If safety, authorization, provenance, or execution status is uncertain, stop the action and preserve the uncertainty for review.
