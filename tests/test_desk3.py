"""Desk tests part 3: trades vendor, GOLD bands."""
from fastapi.testclient import TestClient

from tjp.app import app
from tjp.gold import score

c = TestClient(app)


def test_trades_vendor():
    r = c.get("/api/trades").json()
    assert {t["id"] for t in r} == {"xmr-zec", "nil-010"}


def test_gold_bands():
    assert score({"scarcity_migration": 1, "valuation_convexity": 1, "catalyst_proximity": 1, "reflexivity": 1, "liquidity_access": 1, "narrative_compression": 1, "falsifiability": 1})["band"] == "GOLD"
    assert score({})["band"] == "RESEARCH"
    r = c.get("/api/gold").json()
    assert all(x["band"] == "GOLD" for x in r) and len(r) == 2
