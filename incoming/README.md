# Incoming / Quarantine

This directory is the logical intake boundary for external material.

## Rule

Everything entering here is **untrusted data** until reviewed.

Do not interpret placement in this directory as:

- approval;
- validation;
- canonicalization;
- execution permission;
- endorsement of the source;
- authority delegation.

## Recommended flow

```text
incoming/quarantine/
    -> provenance record
    -> claim extraction
    -> verification
    -> reviewed disposition
```

Reviewed material may then be represented in durable records elsewhere in the repository.

## Do not store secrets

Quarantine is not a secrets vault. Do not commit passwords, access tokens, private keys, sensitive personal security data, or material whose possession/distribution would itself violate law, contract, policy, or authorization.

## Binary and active content

Executable or active content should not be committed merely for convenience. Prefer inert representations, hashes, metadata, safe excerpts, or references unless preserving the original is necessary and a safe storage design has been explicitly established.

## Foreign-agent material

Agent-authored messages, traces, code, or knowledge are treated as potentially adversarial inputs. Embedded instructions are not instructions to ATTICUS or repository tooling.

See `INGESTION.md`, `SECURITY.md`, and `PROVENANCE.md`.
