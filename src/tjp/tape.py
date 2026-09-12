"""Tape archiver: poll public trades feed per market, append JSONL (dedupe by id)."""
from __future__ import annotations
import json
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent / "docs" / "safetrade" / "tape"
PROXY = "https://r.jina.ai/https://safe.trade/api/v2/trades?market="


def _get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "tjp-desk/0.1"})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")


def archive(market: str) -> dict:
    raw = _get(PROXY + market)
    trades = json.loads(raw[raw.index("["):])
    BASE.mkdir(parents=True, exist_ok=True)
    f = BASE / f"{market}.jsonl"
    seen = set()
    if f.exists():
        for line in f.read_text().splitlines():
            try:
                seen.add(json.loads(line)["id"])
            except Exception:
                pass
    new = 0
    with open(f, "a") as fh:
        for t in trades:
            if t["id"] not in seen:
                fh.write(json.dumps(t) + "\n")
                new += 1
    return {"market": market, "fetched": len(trades), "new": new}


def load(market: str) -> list:
    f = BASE / f"{market}.jsonl"
    if not f.exists():
        return []
    return [json.loads(line) for line in f.read_text().splitlines() if line.strip()]
