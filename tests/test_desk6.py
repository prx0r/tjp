"""Desk tests part 6: kill detector."""
from tjp.kill import kill_score, derivative_warnings, lifecycle_stage


def test_kill_score():
    assert kill_score(0, 0, 0, 0, 0, 0) == 0.0
    assert kill_score(1, 1, 1, 1, 1, 1) == 1.0
    assert kill_score(1, 0, 0, 0, 0, 0) == round(1 / 6, 3)


def test_warnings_fire_before_price():
    w = derivative_warnings({
        "demand_growth": [9, 7, 4],
        "utilization": [100, 97, 93],
        "lead_time": [80, 70, 55],
        "inventory": [10, 14, 22],
    })
    assert len(w) == 4


def test_lifecycle():
    assert lifecycle_stage("up", "down", "up", "up", "flat") == "RENT"
    assert lifecycle_stage("flat", "up", "down", "up", "flat") == "HEALING"
    assert lifecycle_stage("flat", "up", "flat", "down", "flat") == "COLLAPSE"
