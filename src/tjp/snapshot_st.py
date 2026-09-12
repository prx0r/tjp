"""SafeTrade snapshot job: markets page via reader proxy → docs/safetrade/snapshots/. No CoinGecko, ever."""
from __future__ import annotations
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent.parent / "docs" / "safetrade" / "snapshots"
ROW = re.compile(r"\[([A-Z0-9]+/[A-Z0-9]+) ([0-9.,]+) ([+-][0-9.]+%) ([0-9.,]+) ([0-9.,]+) ([0-9.,]+) ([0-9.,]+) Trade")
HEAD = re.compile(r"([A-Z0-9]+/[A-Z0-9]+)\s+([+-][0-9.]+%)\s+([0-9.,]+)\s+24h Vol ([0-9.,]+)")


def _f(x: str) -> float:
    return float(x.replace(",", ""))


def fetch_markets() -> str:
    req = urllib.request.Request("https://r.jina.ai/https://safetrade.com/markets",
                                 headers={"User-Agent": "tjp-desk/0.1"})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")


def parse(text: str) -> list:
    rows = {}
    for m in ROW.finditer(text):
        pair, last, chg, hi, lo, amt, vol = m.groups()
        rows[pair] = {"pair": pair, "last": _f(last), "chg_24h": chg, "high": _f(hi),
                      "low": _f(lo), "amount_24h": _f(amt), "volume_24h": _f(vol)}
    for m in HEAD.finditer(text):
        pair, chg, last, vol = m.groups()
        rows.setdefault(pair, {"pair": pair, "last": _f(last), "chg_24h": chg, "high": None,
                               "low": None, "amount_24h": None, "volume_24h": _f(vol)})
    return list(rows.values())


def snapshot() -> dict:
    try:
        rows = parse(fetch_markets())
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}
    if not rows:
        return {"ok": False, "error": "no rows parsed"}
    OUT.mkdir(parents=True, exist_ok=True)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M")
    (OUT / f"{day}.json").write_text(json.dumps(
        {"ts": datetime.now(timezone.utc).isoformat(), "n": len(rows), "rows": rows}, indent=1))
    return {"ok": True, "n": len(rows), "file": f"{day}.json"}
