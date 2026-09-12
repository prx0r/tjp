"""Positions log: paper-only open-position records per thesis. No real money, no chain writes."""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

_STORE = Path(__file__).resolve().parent.parent.parent / "docs" / "positions.json"


def _load() -> list:
    if _STORE.exists():
        return json.loads(_STORE.read_text())
    return []


def _save(rows: list) -> None:
    _STORE.parent.mkdir(parents=True, exist_ok=True)
    _STORE.write_text(json.dumps(rows, indent=1))


def log_position(thesis_id: str, thesis_n: int, action: str, note: str = "") -> dict:
    row = {
        "thesis_id": thesis_id,
        "thesis_n": thesis_n,
        "action": action,
        "note": note,
        "mode": "paper",
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    rows = _load()
    rows.append(row)
    _save(rows)
    return row


def positions_for(thesis_id: str) -> list:
    return [r for r in _load() if r["thesis_id"] == thesis_id]
