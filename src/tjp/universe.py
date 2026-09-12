"""Universe tracker: diff live markets list vs stored universe → listing/delist events.
Dead markets are retained forever (survivorship guard)."""
from __future__ import annotations
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent / "docs" / "safetrade"
EVENTS = BASE / "universe_events.jsonl"


def _get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "tjp-desk/0.1"})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")


def fetch_markets() -> list:
    raw = _get("https://r.jina.ai/https://safe.trade/api/v2/markets")
    return json.loads(raw[raw.index("["): ])


def diff() -> dict:
    live = {m["id"]: m for m in fetch_markets()}
    uni = json.load(open(BASE / "universe.json"))
    old = {m["id"]: m for m in uni["markets"]}
    events = []
    for mid, m in live.items():
        if mid not in old:
            events.append({"type": "new_market", "id": mid, "state": m.get("state"),
                           "created_at": m.get("created_at")})
        elif old[mid].get("state") != m.get("state"):
            events.append({"type": "state_change", "id": mid,
                           "was": old[mid].get("state"), "now": m.get("state")})
    for mid in old:
        if mid not in live:
            events.append({"type": "removed_market", "id": mid, "was": old[mid].get("state")})
    if events:
        with open(EVENTS, "a") as fh:
            for e in events:
                e["detected"] = datetime.now(timezone.utc).isoformat()
                fh.write(json.dumps(e) + "\n")
    return {"new": sum(1 for e in events if e["type"] == "new_market"),
            "state_changes": sum(1 for e in events if e["type"] == "state_change"),
            "removed": sum(1 for e in events if e["type"] == "removed_market"),
            "events": events}
