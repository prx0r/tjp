"""Desk tests part 4: funnel, falsifiers, catalysts, snapshots."""
from fastapi.testclient import TestClient

from tjp.app import app

c = TestClient(app)


def test_funnel_advance_and_guard():
    assert c.get("/api/funnel").json()["stages"][0] == "DISCOVER"
    r = c.post("/api/funnel/xmr-zec", params={"to": "FUNDAMENTAL", "note": "t"}).json()
    assert r["stage"] == "FUNDAMENTAL"
    assert "error" in c.post("/api/funnel/xmr-zec", params={"to": "DISCOVER"}).json()
    assert "error" in c.post("/api/funnel/xmr-zec", params={"to": "NOPE"}).json()


def test_falsifiers_flow():
    lst = c.get("/api/falsifiers/xmr-zec").json()
    assert len(lst) >= 1 and lst[0]["status"] == "open"
    assert c.post("/api/falsifiers/xmr-zec/0", params={"status": "triggered"}).json()["status"] == "triggered"
    assert c.get("/api/falsifiers/xmr-zec").json()[0]["status"] == "triggered"
    c.post("/api/falsifiers/xmr-zec/0", params={"status": "open"})


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
