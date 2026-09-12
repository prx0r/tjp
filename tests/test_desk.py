"""Desk tests: inventory sees both vendors; API health green (no vendor execution)."""
from fastapi.testclient import TestClient

from tjp import app as _  # noqa: F401  (import check only)


def test_inventory_counts():
    from tjp.desk import inventory

    inv = inventory()
    assert len(inv["blueprint"]) >= 15
    assert len(inv["kernel"]) >= 30


def test_health():
    from tjp.app import app

    c = TestClient(app)
    assert c.get("/api/health").json() == {"ok": True}
    assert c.get("/api/inventory").json()["blueprint"] >= 15
