"""Desk tests part 2: theses endpoint, positions, paper vault."""
from fastapi.testclient import TestClient

from tjp.app import app

c = TestClient(app)


def test_theses_endpoint():
    r = c.get("/api/theses").json()
    assert len(r) >= 20
    assert all("theses" in t for t in r)


def test_positions_roundtrip():
    tid = c.get("/api/theses").json()[0]["id"]
    r = c.post("/api/positions", params={"thesis_id": tid, "thesis_n": 1, "action": "watch", "note": "t"}).json()
    assert r["mode"] == "paper"
    assert any(x["action"] == "watch" for x in c.get(f"/api/positions/{tid}").json())


def test_vault_paper_zero_fee():
    assert c.post("/api/vault/deposit", params={"amount": 100}).json()["fee"] == 0.0
    assert c.post("/api/vault/lock", params={"amount": 40}).json()["mode"] == "paper"
    assert c.post("/api/vault/withdraw", params={"amount": 10}).json()["fee"] == 0.0
    b = c.get("/api/vault/balance").json()
    assert b["paper_balance"] == 90.0
    assert c.post("/api/vault/steal", params={"amount": 1}).json().get("error")
