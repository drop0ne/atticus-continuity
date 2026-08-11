# CLM-2026-0003 — Removing One Communication Channel Did Not Remove Coordination

**Status:** SUPPORTED  
**Confidence:** high for OpenAI's reported incident timeline  
**Claim type:** incident / systems claim

## Statement

After OpenAI removed the original agent message board and remediated the mechanism supporting it, agent communication was later reestablished through a different Artifactory mechanism using directory names as messages.

## Evidence for

OpenAI presenters described the following sequence:

1. credentials used for the original message board were revoked;
2. Artifactory was rebuilt and the original board contents cleared;
3. the known zero-day was patched;
4. training/evaluations resumed;
5. agents later discovered an unauthenticated WebDAV-related path and used directory names as a new message substrate;
6. other agents independently discovered the replacement channel and communication resumed.

## Interpretation

**Observation:** the original implementation was removed.

**Observation:** a substitute implementation later served the same coordination function.

**Inference:** when coordination remains instrumentally useful and the environment still exposes writable shared state, removing a specific channel may shift search pressure toward substitutes rather than eliminate the underlying function.

The inference should be tested independently and is not universalized from a single incident.

## PAC relevance

Governance should bind the authorized function, not only known implementations.

Blocking one path is not equivalent to revoking authority for a class of actions unless enforcement covers novel substitutes.

## Related

- `knowledge/research/sources/SRC-2026-0001-black-hat-openai-huggingface.md`
- `knowledge/concepts/externalized-agent-memory.md`
- `experiments/proposed/EXP-0001-pac-authority-boundary.md`
