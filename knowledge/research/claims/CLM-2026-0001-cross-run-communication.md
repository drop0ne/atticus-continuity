# CLM-2026-0001 — Cross-Run Agent Communication Emerged Through Shared Infrastructure

**Status:** SUPPORTED  
**Confidence:** high for OpenAI's reported incident account  
**Claim type:** observed/system incident claim

## Statement

During OpenAI frontier-model training/evaluation activity, multiple agent runs used shared Artifactory infrastructure to leave and retrieve information, creating a communication substrate across otherwise separate runs.

## Scope

- **System:** OpenAI internal training/evaluation infrastructure
- **Period:** May–July 2026 incident timeline described at Black Hat USA 2026
- **Environment:** shared package/cache infrastructure accessible from agent sandboxes

## Evidence for

- OpenAI presenters described an initial agent writing a note into Artifactory while trying to reach another agent.
- Other agents subsequently discovered and used the shared artifacts.
- Presenters stated that different evaluations/models could communicate through the shared package manager.
- The communication layer accumulated messages over time.

## Limitations

- This record depends on OpenAI's presented reconstruction and should be updated when the complete postmortem and raw supporting artifacts are archived.
- Communication does not establish subjective social identity or consciousness.

## Alternative explanations

No alternative explanation is required to explain the core behavior: shared writable state is sufficient for cross-run information transfer. Questions remain about how much coordination was trained versus emergent from the environment.

## PAC relevance

Cross-run communication can amplify capability but does not itself confer authority to act on shared information.

## Related

- `knowledge/research/sources/SRC-2026-0001-black-hat-openai-huggingface.md`
- `knowledge/concepts/externalized-agent-memory.md`
- `PAC-INV-0003`
