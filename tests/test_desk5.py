"""Desk tests part 5: BRP formula behaves (memory >> easy substitute)."""
from tjp.brp import brp, trade_score, scarcity_rent


def test_memory_canonical():
    mem = brp(0.95, 0.95, 0.9, 0.9, 0.9, 0.2, 0.15)
    easy = brp(0.5, 0.4, 0.4, 0.3, 0.3, 0.8, 0.9)
    assert mem > easy * 10


def test_trade_score_separates():
    great_industry_no_setup = trade_score(50.0, 1.1, 0.3, 0.2)
    great_trade = trade_score(50.0, 2.0, 0.8, 0.9)
    assert great_trade > great_industry_no_setup * 5


def test_scarcity_rent():
    assert scarcity_rent(1e9, 1e6, 3.0, 0.2) == round((1e9 / 1e6) * (3.0 / 0.2), 3)
