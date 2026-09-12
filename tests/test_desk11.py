"""Desk tests part 11: router edges + strategy engine."""
from fastapi.testclient import TestClient

from tjp.app import app
from tjp.router import edges, inference_edges
from tjp.strategy import cross_signals, run_strategy

c = TestClient(app)


def test_router_ranks_positive_first():
    es = edges()
    assert es and es[0]["edge_day"] >= es[-1]["edge_day"]
    assert any(e["edge_day"] > 0 for e in es)
    assert inference_edges()[0]["per_1usd"] >= inference_edges()[-1]["per_1usd"]


def test_strategy_trend_captures():
    prices = [100 + i for i in range(30)] + [130 - i for i in range(30)]
    sig = cross_signals(prices, 3, 10)
    r = run_strategy(prices, sig)
    assert r["trades"] >= 1 and r["bars"] == 60
    assert set(r) >= {"total_ret", "sharpe_like", "max_drawdown", "win_rate", "equity_end"}


def test_strategy_flat_costs_drag():
    r = run_strategy([1.0] * 20, [1] * 20, fee_bps=100)
    assert r["total_ret"] < 0


def test_router_endpoint():
    assert len(c.get("/api/router/edges").json()["edges"]) >= 5
