#!/usr/bin/env python3
"""Deterministic PAC DOCX/SVG text projection for source-preservation work.

Input is a recovered PAC TAR. Output is a directory of per-member UTF-8 text
projections plus index.json. The extractor is inert/read-only with respect to
source bytes. It does not execute macros, external links, or embedded content.
"""
from __future__ import annotations
import argparse, hashlib, io, json, re, tarfile, zipfile
from pathlib import Path
from lxml import etree
from docx import Document

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
TEXT_PARTS = {"word/document.xml", "word/footnotes.xml", "word/endnotes.xml", "word/comments.xml"}
LABEL = re.compile(r"^(?P<label>(?:[IVX]+|0|[A-F])\.\d+[A-Za-z]?)\b")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def _parts(z: zipfile.ZipFile) -> list[str]:
    out = []
    for name in z.namelist():
        if name in TEXT_PARTS or re.fullmatch(r"word/(header|footer)\d+\.xml", name):
            out.append(name)
    return sorted(out, key=lambda n: (0 if n == "word/document.xml" else 1, n))


def _xml_text(raw: bytes) -> str:
    root = etree.fromstring(raw)
    lines = []
    for p in root.iter(W + "p"):
        chunks = []
        for node in p.iter():
            if node.tag == W + "t" and node.text:
                chunks.append(node.text)
            elif node.tag == W + "tab":
                chunks.append("\t")
            elif node.tag in (W + "br", W + "cr"):
                chunks.append("\n")
            elif node.tag == W + "noBreakHyphen":
                chunks.append("-")
            elif node.tag == W + "softHyphen":
                chunks.append("\u00ad")
        lines.append("".join(chunks))
    return "\n".join(lines)


def _docx_projection(data: bytes) -> tuple[str, list[dict], list[dict], list[dict]]:
    chunks, parts = [], []
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for name in _parts(z):
            raw = z.read(name)
            text = _xml_text(raw)
            chunks.append(f"===== BEGIN {name} =====\n{text}\n===== END {name} =====\n")
            parts.append({
                "part": name,
                "xml_sha256": sha256(raw),
                "extracted_text_sha256": sha256(text.encode("utf-8")),
                "chars": len(text),
            })
    doc = Document(io.BytesIO(data))
    headings, labels = [], {}
    for i, p in enumerate(doc.paragraphs, 1):
        text = p.text.strip()
        style = p.style.name if p.style else ""
        if text and (style.lower().startswith("heading") or style.lower() in ("title", "subtitle")):
            headings.append({"paragraph_index": i, "style": style, "text": text})
        m = LABEL.match(text)
        if m:
            labels.setdefault(m.group("label"), []).append({"paragraph_index": i, "style": style, "text": text})
    numbered = [{
        "label": label,
        "occurrences": occ,
        "heading_style_present": any(o["style"].lower().startswith("heading") for o in occ),
    } for label, occ in labels.items()]
    return "".join(chunks), parts, headings, numbered


def extract(tar_path: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    tar_bytes = tar_path.read_bytes()
    index = {
        "schema_version": "1.0",
        "source_tar_size_bytes": len(tar_bytes),
        "source_tar_sha256": sha256(tar_bytes),
        "extraction_method": "WordprocessingML paragraph text in XML order; selected text-bearing parts; no editorial rewriting; formatting not preserved",
        "members": [],
    }
    with tarfile.open(tar_path, "r") as tf:
        for logical_index, member in enumerate((m for m in tf.getmembers() if m.isfile()), 1):
            data = tf.extractfile(member).read()
            record = {
                "tar_member_index": logical_index,
                "path_in_tar": member.name,
                "source_size_bytes": len(data),
                "source_sha256": sha256(data),
            }
            if member.name.endswith(".docx"):
                text, parts, headings, numbered = _docx_projection(data)
                name = f"tar-{logical_index:02d}.txt"
                payload = text.encode("utf-8")
                (out_dir / name).write_bytes(payload)
                record.update({"projection_path": name, "projection_sha256": sha256(payload), "projection_git_blob_sha1": git_blob_sha1(payload), "parts": parts, "headings": headings, "numbered_label_occurrences": numbered})
            elif member.name.endswith(".svg"):
                data.decode("utf-8")
                name = f"tar-{logical_index:02d}.svg"
                (out_dir / name).write_bytes(data)
                record.update({"projection_path": name, "projection_sha256": sha256(data), "projection_git_blob_sha1": git_blob_sha1(data), "projection": "verbatim_utf8"})
            index["members"].append(record)
    index_bytes = (json.dumps(index, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    (out_dir / "index.json").write_bytes(index_bytes)
    return index


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("tar", type=Path)
    ap.add_argument("out", type=Path)
    args = ap.parse_args()
    idx = extract(args.tar, args.out)
    print(json.dumps({"source_tar_sha256": idx["source_tar_sha256"], "members": len(idx["members"])}))

if __name__ == "__main__":
    main()
