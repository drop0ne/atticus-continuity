# Source Integrity Verifier

`REF-SRC-INT-0001` is a read-only, standard-library SHA-256 verifier for preserved ATTICUS/PAC artifacts.

It never executes, parses as code, or modifies the artifact being verified. It reads bytes only.

## Verify one file

```bash
python -m reference.source_integrity.verify file \
  /path/to/artifact \
  --sha256 <64-hex-digest> \
  --size <expected-byte-count>
```

Exit codes:

- `0` — hash and optional size match;
- `1` — artifact exists/was checked but verification failed;
- `2` — malformed verification request or unsafe manifest input.

Output is JSON so results can be preserved as evidence.

## Verify a JSON manifest

```bash
python -m reference.source_integrity.verify manifest manifest.json
```

Schema:

```json
{
  "schema_version": "1.0",
  "artifacts": [
    {
      "path": "relative/path/to/source.bin",
      "sha256": "<64 hex>",
      "size_bytes": 123
    }
  ]
}
```

Manifest paths are relative to the manifest directory unless `--root` is supplied. Absolute paths, duplicate paths, and paths escaping the verification root are rejected.

## PAC example

When the recovered PAC TAR is available locally:

```bash
python -m reference.source_integrity.verify file \
  'PAC_FIRST_EDITION_DEFINITIVE(20260823-114607).tar' \
  --sha256 2198f146bc56fe97d754a4e87bf1ecd9c3f03050b1ace2b215b5169c62b9a9a8 \
  --size 931840
```

This validates the recovered uncompressed TAR payload only. It does not establish identity of the historically named `.tar.gz` wrapper.

## ATTICUS use

When raw Library bytes for the duplicate Markdown/DOCX candidates become available, run this verifier against each exact byte stream before collapsing duplicate identities or selecting a preserved canonical source artifact.

## Security boundary

- read-only bytes in;
- digest/size evidence out;
- no network capability;
- no archive extraction;
- no macro execution;
- no document rendering;
- no source canonicalization.

A PASS proves only that the checked byte stream matches the supplied expected digest/size. It does not prove provenance, authorship, correctness, or canonical authority.
