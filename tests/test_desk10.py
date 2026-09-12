"""Desk tests part 10: history, runner, backtest endpoints, survivorship."""
from fastapi.testclient import TestClient

from tjp.app import app
from tjp.history import tape_series

c = TestClient(app)


def test_history_from_tape():
    import json
    from pathlib import Path

    f = Path("/tjp/docs/safetrade/tape/_test.jsonl")
    f.parent.mkdir(parents=True, exist_ok=True)
    rows = [{"id": i, "price": str(1.0 + i * 0.1), "created_at": f"2026-09-12T15:{i:02d}:00Z"} for i in range(5)]
    f.write_text("\n".join(json.dumps(r) for r in rows))
    try:
        s = tape_series("_test")
        assert len(s) == 5 and s[0][0] <= s[-1][0]
    finally:
        f.unlink(missing_ok=True)


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
    import json
    from pathlib import Path

    f = Path("/tjp/docs/safetrade/tape/_ep.jsonl")
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps({"id": 1, "price": "0.5", "created_at": "2026-09-12T15:00:00Z"}))
    try:
        r = c.get("/api/backtest/history/_ep").json()
        assert r["points"] == 1
    finally:
        f.unlink(missing_ok=True)
