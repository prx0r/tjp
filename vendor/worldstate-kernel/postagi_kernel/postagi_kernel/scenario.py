from __future__ import annotations
import math
from dataclasses import replace
from .models import Scenario, Evidence


def logit(p: float) -> float:
    p = min(max(float(p), 1e-9), 1-1e-9)
    return math.log(p/(1-p))


def logistic(x: float) -> float:
    return 1/(1+math.exp(-x))


def bayesian_update(prior: float, evidence: list[Evidence]) -> float:
    """Odds-form Bayes update from evidence log-likelihood ratios.

    Reliability in [0,1] tempers each evidence contribution, mitigating
    correlated/noisy sources when a full dependency model is unavailable.
    """
    l = logit(prior)
    for e in evidence:
        l += e.log_likelihood_ratio * max(0.0, min(1.0, e.reliability))
    return logistic(l)


def update_scenario(s: Scenario, evidence: list[Evidence]) -> Scenario:
    matched = [e for e in evidence if e.target_scenario == s.id]
    return replace(s, our_probability=bayesian_update(s.our_probability, matched))
