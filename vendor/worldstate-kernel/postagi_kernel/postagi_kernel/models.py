from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Iterable, Mapping

@dataclass(frozen=True)
class Scenario:
    id: str
    name: str
    horizon_years: float
    our_probability: float
    market_probability: float
    description: str = ""

    @property
    def divergence(self) -> float:
        return self.our_probability - self.market_probability

@dataclass
class Company:
    ticker: str
    name: str
    sector: str
    cashflow_duration: float = 1.0
    technological_duration: float = 1.0
    exposures: Dict[str, float] = field(default_factory=dict)
    evidence_confidence: float = 1.0

@dataclass
class Evidence:
    id: str
    timestamp: str
    source_type: str
    target_scenario: str
    log_likelihood_ratio: float
    reliability: float = 1.0
    description: str = ""

@dataclass
class ScoreBreakdown:
    ticker: str
    scenario_components: Dict[str, float]
    divergence_score: float
    obsolescence_score: float
    convergence_score: float
    patentomics_score: float
    total_score: float
