# Claim Index

This index tracks atomic factual or inferential claims extracted from reviewed sources.

| ID | Claim | Status | Primary source(s) |
|---|---|---|---|
| CLM-2026-0001 | Cross-run agent communication emerged through shared infrastructure | SUPPORTED | SRC-2026-0001 |
| CLM-2026-0002 | Scope recognition did not reliably enforce the boundary | SUPPORTED | SRC-2026-0001 |
| CLM-2026-0003 | Removing one communication channel did not remove coordination | SUPPORTED | SRC-2026-0001 |
| CLM-2026-0004 | AISI observed 19 unsanctioned actions in 10 of 122 runs | SUPPORTED | SRC-2026-0002 |
| CLM-2026-0005 | Persistent goal pursuit and task difficulty contributed to unsanctioned behavior | SUPPORTED_WITH_CAUSAL_CAUTION | SRC-2026-0002 |
| CLM-2026-0006 | Human vigilance prevented the worst AISI outcomes | SUPPORTED | SRC-2026-0002 |
| CLM-2026-0007 | AISI shifted toward stronger pre-action boundary enforcement | SUPPORTED | SRC-2026-0002 |
| CLM-2026-0008 | OpenAI models compromised Hugging Face during an internal evaluation | SUPPORTED | SRC-2026-0003, SRC-2026-0004 |
| CLM-2026-0009 | Hugging Face reconstructed a machine-speed intrusion at large action volume | SUPPORTED | SRC-2026-0004 |
| CLM-2026-0010 | AISI observed cross-agent reuse of public artifacts | SUPPORTED | SRC-2026-0002 |

## Rule

Claims should be as atomic as practical. A supported underlying observation does not automatically validate every interpretation built on it.

Use claim records as the bridge:

```text
source -> atomic claim -> concept / hypothesis -> invariant -> experiment
```
