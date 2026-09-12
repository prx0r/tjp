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
    cal = c.get("/api/catalysts").json()
    assert any("2027-02-18" in x["date"] for x in cal if x["date"])
    s = c.get("/api/snapshots/latest").json()
    assert s["ok"] is True and "monero" in s["prices"]
