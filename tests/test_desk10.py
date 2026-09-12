"""Desk tests part 10: history, runner, backtest endpoints, survivorship."""
from fastapi.testclient import TestClient

from tjp.app import app
from tjp.history import tape_series

c = TestClient(app)


def test_history_from_tape():
    s = tape_series("prlusdt")
    assert len(s) == 100 and s[0][0] <= s[-1][0]


def test_runner_report_shape():
    r = c.get("/api/backtest/report").json()
    assert len(r["listings"]) >= 15 and r["cohort"]["n"] == 0
    assert all(g["passed"] == 0 for g in r["gates"])


def test_survivorship_retained():
    import json

    uni = json.load(open("/tjp/docs/safetrade/universe.json"))
    states = {m["state"] for m in uni["markets"]}
    assert "disabled" in states  # dead markets stay in the universe
    lst = c.get("/api/backtest/listings").json()
    assert any(l["asset"] == "PRL" for l in lst)


def test_history_endpoint():
    r = c.get("/api/backtest/history/prlusdt").json()
    assert r["points"] == 100
