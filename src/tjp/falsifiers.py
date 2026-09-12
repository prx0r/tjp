"""Falsifier checklist: explicit wrongness conditions per trade. Triggered = exit review."""
from __future__ import annotations
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent


def falsifiers_for(trade_id: str) -> list:
    d = json.loads((BASE / "vendor" / "thesisdesk" / "data" / "trades.json").read_text())
    for t in d.get("trades", []):
        if t["id"] == trade_id:
            st = _states().get(trade_id, {})
            return [{"text": f, "status": st.get(str(i), "open")} for i, f in enumerate(t.get("falsifiers", []))]
    return []


def _states() -> dict:
    f = BASE / "docs" / "falsifiers.json"
    return json.loads(f.read_text()) if f.exists() else {}


def set_status(trade_id: str, idx: int, status: str) -> dict:
    assert status in ("open", "triggered", "cleared")
    f = BASE / "docs" / "falsifiers.json"
    d = _states()
    d.setdefault(trade_id, {})[str(idx)] = status
    f.write_text(json.dumps(d, indent=1))
    return {"trade_id": trade_id, "idx": idx, "status": status}
