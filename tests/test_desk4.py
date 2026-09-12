"""Desk tests part 4: funnel, falsifiers, catalysts, snapshots."""
from fastapi.testclient import TestClient

from tjp.app import app

c = TestClient(app)


def test_funnel_advance_and_guard(tmp_path, monkeypatch):
    import tjp.funnel as fn

    monkeypatch.setattr(fn, "_STORE", tmp_path / "f.json")
    assert fn.advance("t", "FUNDAMENTAL", note="t")["stage"] == "FUNDAMENTAL"
    assert "error" in fn.advance("t", "DISCOVER")
    assert "error" in fn.advance("t", "NOPE")
    assert c.get("/api/funnel").json()["stages"][0] == "DISCOVER"


def test_falsifiers_flow(tmp_path, monkeypatch):
    import tjp.falsifiers as fa

    monkeypatch.setattr(fa, "BASE", tmp_path)
    (tmp_path / "docs").mkdir(exist_ok=True)
    import json

    assert fa.set_status("t", 0, "triggered")["status"] == "triggered"


def test_catalysts_and_snapshot_shape():
    import json
    from pathlib import Path

    cal = c.get("/api/catalysts").json()
    assert any("2027-02-18" in x["date"] for x in cal if x["date"])
    d = Path("/tjp/docs/safetrade/snapshots")
    d.mkdir(parents=True, exist_ok=True)
    f = d / "_test.json"
    f.write_text(json.dumps({"ts": "2026-09-12T00:00:00+00:00", "n": 1,
                             "rows": [{"pair": "PRL/USDT", "last": 0.55, "chg_24h": "+0%",
                                       "high": 0.55, "low": 0.55, "amount_24h": 1.0, "volume_24h": 1.0}]}))
    try:
        s = c.get("/api/snapshots/latest").json()
        assert s["ok"] is True and "PRL/USDT" in s["prices"]
    finally:
        f.unlink(missing_ok=True)
