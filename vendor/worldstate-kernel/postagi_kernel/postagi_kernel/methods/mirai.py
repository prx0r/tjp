"""MIRAI-inspired temporal event forecasting interface.

MIRAI models forecasting as retrieval over historical structured events + text,
followed by iterative reasoning/tool use. Here we expose the data-contract and a
fully deterministic frequency/recency baseline so the surrounding kernel can be
tested without an LLM API. Swap `forecast` with an agent implementing the same
interface for paper-style ReAct experiments.
"""
from __future__ import annotations
from collections import defaultdict
import math

class TemporalEventForecaster:
    def __init__(self, decay_half_life_days: float = 180.0):
        self.half_life = decay_half_life_days

    def forecast(self, events: list[dict], relation_key: str, asof_day: int) -> dict[str, float]:
        scores = defaultdict(float)
        lam = math.log(2) / self.half_life
        for e in events:
            day = int(e["day"])
            if day > asof_day:
                continue
            age = asof_day - day
            scores[str(e[relation_key])] += math.exp(-lam * age)
        z = sum(scores.values()) or 1.0
        return {k: v/z for k,v in scores.items()}
