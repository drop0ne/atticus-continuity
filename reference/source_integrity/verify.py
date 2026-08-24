"""Deterministic SHA-256 verification for preserved source artifacts.

Standard-library only. Imported artifacts are read as bytes and never executed.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, sys
from dataclasses import dataclass, asdict
from pathlib import Path
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
DEFAULT_CHUNK_SIZE = 1024 * 1024
class VerificationError(ValueError):
    pass
@dataclass(frozen=True)
class VerificationResult:
    path: str
    expected_sha256: str
    actual_sha256: str | None
    expected_size_bytes: int | None
    actual_size_bytes: int | None
    sha256_match: bool
    size_match: bool | None
    status: str
    error: str | None = None
    @property
    def ok(self) -> bool:
        return self.status == "PASS"
def _normalize_sha256(value: str) -> str:
    if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
        raise VerificationError("expected SHA-256 must be exactly 64 hexadecimal characters")
    return value.lower()
def sha256_file(path: os.PathLike[str] | str, chunk_size: int = DEFAULT_CHUNK_SIZE) -> tuple[str, int]:
    if chunk_size <= 0:
        raise VerificationError("chunk_size must be positive")
    p = Path(path); h = hashlib.sha256(); size = 0
    with p.open("rb") as fh:
        while True:
            block = fh.read(chunk_size)
            if not block: break
            size += len(block); h.update(block)
    return h.hexdigest(), size
def verify_file(path, expected_sha256: str, expected_size_bytes: int | None = None) -> VerificationResult:
    expected = _normalize_sha256(expected_sha256)
    if expected_size_bytes is not None and (not isinstance(expected_size_bytes, int) or isinstance(expected_size_bytes, bool) or expected_size_bytes < 0):
        raise VerificationError("expected_size_bytes must be a non-negative integer")
    p = Path(path); display = str(p)
    try:
        if not p.is_file():
            return VerificationResult(display, expected, None, expected_size_bytes, None, False, None if expected_size_bytes is None else False, "FAIL", "path is not a regular file")
        actual_hash, actual_size = sha256_file(p)
    except OSError as exc:
        return VerificationResult(display, expected, None, expected_size_bytes, None, False, None if expected_size_bytes is None else False, "FAIL", f"{type(exc).__name__}: {exc}")
    hash_ok = actual_hash == expected
    size_ok = None if expected_size_bytes is None else actual_size == expected_size_bytes
    ok = hash_ok and (size_ok is not False)
    return VerificationResult(display, expected, actual_hash, expected_size_bytes, actual_size, hash_ok, size_ok, "PASS" if ok else "FAIL", None)
def _safe_manifest_path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative:
        raise VerificationError("artifact path must be a non-empty string")
    rel = Path(relative)
    if rel.is_absolute():
        raise VerificationError(f"manifest artifact path must be relative: {relative!r}")
    rr = root.resolve(); candidate = (rr / rel).resolve()
    try: candidate.relative_to(rr)
    except ValueError as exc: raise VerificationError(f"artifact path escapes verification root: {relative!r}") from exc
    return candidate
def verify_manifest(manifest_path, root=None) -> dict:
    mpath = Path(manifest_path)
    try: data = json.loads(mpath.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc: raise VerificationError(f"cannot read JSON manifest: {exc}") from exc
    if not isinstance(data, dict): raise VerificationError("manifest root must be a JSON object")
    if data.get("schema_version") != "1.0": raise VerificationError("unsupported or missing schema_version; expected '1.0'")
    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts: raise VerificationError("manifest artifacts must be a non-empty array")
    root_path = Path(root) if root is not None else mpath.parent
    seen=set(); results=[]
    for index,item in enumerate(artifacts):
        if not isinstance(item, dict): raise VerificationError(f"artifact[{index}] must be an object")
        rel=item.get("path")
        if rel in seen: raise VerificationError(f"duplicate artifact path: {rel!r}")
        seen.add(rel)
        candidate=_safe_manifest_path(root_path, rel)
        results.append(verify_file(candidate, item.get("sha256"), item.get("size_bytes")))
    passed=sum(r.ok for r in results); failed=len(results)-passed
    return {"schema_version":"1.0","manifest":str(mpath),"verification_root":str(root_path.resolve()),"artifact_count":len(results),"passed":passed,"failed":failed,"status":"PASS" if failed==0 else "FAIL","results":[asdict(r)|{"ok":r.ok} for r in results]}
def _emit(payload):
    json.dump(payload, sys.stdout, indent=2, sort_keys=True); sys.stdout.write("\n")
def _build_parser():
    p=argparse.ArgumentParser(description="Read-only SHA-256 verification for ATTICUS/PAC source artifacts.")
    sub=p.add_subparsers(dest="command", required=True)
    one=sub.add_parser("file", help="verify one file"); one.add_argument("path"); one.add_argument("--sha256", required=True, dest="expected_sha256"); one.add_argument("--size", type=int, default=None, dest="expected_size_bytes")
    man=sub.add_parser("manifest", help="verify a JSON integrity manifest"); man.add_argument("manifest"); man.add_argument("--root", default=None)
    return p
def main(argv=None):
    args=_build_parser().parse_args(argv)
    try:
        if args.command=="file":
            r=verify_file(args.path,args.expected_sha256,args.expected_size_bytes); _emit({"status":r.status,"result":asdict(r)|{"ok":r.ok}}); return 0 if r.ok else 1
        s=verify_manifest(args.manifest,args.root); _emit(s); return 0 if s["status"]=="PASS" else 1
    except VerificationError as exc:
        _emit({"status":"ERROR","error":str(exc)}); return 2
if __name__=="__main__": raise SystemExit(main())
