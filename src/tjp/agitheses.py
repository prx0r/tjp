"""agitheses: memos → structured JSON. Reads agents@ .eml backlog, writes docs/agitheses/*.json."""
from __future__ import annotations
import email
import json
import re
from pathlib import Path

HEAD_RE = re.compile(r"^\s*(\d+)[.)]\s+(.+)$", re.M)
RATE_RE = re.compile(r"(\d+(?:\.\d+)?)/10")
FALS_RE = re.compile(r"^\s*\*?Falsifiers?:\*?\s*(.+)$", re.M | re.I)


def parse_memo(path: Path) -> dict:
    from email.header import decode_header, make_header

    m = email.message_from_binary_file(open(path, "rb"))
    subj = str(make_header(decode_header(str(m["Subject"]))))
    body = ""
    for p in m.walk():
        if p.get_content_type() == "text/plain" and not p.get_filename():
            body = p.get_payload(decode=True).decode("utf-8", "replace")
            break
    kind = "alpha_hunt" if "Alpha Hunt" in subj else ("kernel_build" if "Kernel" in subj else "research_memo")
    # executive view = text between "Executive view" and first numbered heading
    summary = ""
    if "Executive view" in body:
        summary = body.split("Executive view", 1)[1]
        mh = HEAD_RE.search(summary)
        if mh:
            summary = summary[: mh.start()].strip()
    summary = " ".join(summary.split())[:1200]
    theses = []
    heads = list(HEAD_RE.finditer(body))
    for i, h in enumerate(heads):
        chunk = body[h.start() : heads[i + 1].start() if i + 1 < len(heads) else len(body)]
        rate = RATE_RE.search(chunk)
        fals = FALS_RE.search(chunk)
        theses.append(
            {
                "n": int(h.group(1)),
                "title": h.group(2).strip()[:200],
                "rating": float(rate.group(1)) if rate else None,
                "falsifier": fals.group(1).strip()[:500] if fals else None,
                "body": " ".join(chunk.strip().split())[:2000],
            }
        )
    return {
        "id": path.stem,
        "subject": subj,
        "date": str(m["Date"]),
        "kind": kind,
        "executive_summary": summary,
        "theses": theses,
    }


def build(src_dir: Path, out_dir: Path) -> list[str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    ids = []
    for f in sorted(src_dir.glob("*.eml")):
        d = parse_memo(f)
        (out_dir / f"{d['id']}.json").write_text(json.dumps(d, indent=1))
        ids.append(d["id"])
    return ids


SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "agithesis",
    "type": "object",
    "required": ["id", "subject", "date", "kind", "theses"],
    "properties": {
        "id": {"type": "string"},
        "subject": {"type": "string"},
        "date": {"type": "string"},
        "kind": {"enum": ["research_memo", "alpha_hunt", "kernel_build"]},
        "executive_summary": {"type": "string"},
        "theses": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["n", "title", "body"],
                "properties": {
                    "n": {"type": "integer"},
                    "title": {"type": "string"},
                    "rating": {"type": ["number", "null"]},
                    "body": {"type": "string"},
                },
            },
        },
    },
}
