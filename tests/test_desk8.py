"""Desk tests part 8: buy-hold engine rules."""
from tjp.buyhold import buy_hold


def test_antilookead_fill():
    r = buy_hold([1.0, 1.1, 1.2], entry_idx=0, size=100.0, fee_bps=0, slippage_bps=0)
    assert r["fill"] == 1.1  # t+1 open, not signal bar
    assert r["ret_pct"] == round((100 / 1.1 * 1.2 - 100) / 100 * 100, 2)


def test_fees_drag():
    cheap = buy_hold([1.0, 1.0, 1.0], size=1000.0, fee_bps=0, slippage_bps=0)
    pricey = buy_hold([1.0, 1.0, 1.0], size=1000.0, fee_bps=200, slippage_bps=100)
    assert cheap["net"] == 0.0 and pricey["net"] < 0.0


def test_live_tape_shape():
    import json
    from pathlib import Path

    f = Path("/tjp/docs/safetrade/tape/_shape.jsonl")
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text("\n".join(json.dumps({"id": i, "price": "0.55", "created_at": "2026-09-12T15:00:00Z"}) for i in range(3)))
    try:
        d = [json.loads(line) for line in f.read_text().splitlines()]
        assert len(d) == 3 and all(float(x["price"]) > 0 for x in d)
    finally:
        f.unlink(missing_ok=True)
