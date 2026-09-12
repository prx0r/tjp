from __future__ import annotations
from typing import Iterable
import numpy as np
import pandas as pd
from .models import Scenario, Company, ScoreBreakdown


def world_divergence_score(company: Company, scenarios: Iterable[Scenario]) -> tuple[float, dict[str,float]]:
    parts = {}
    for s in scenarios:
        impact = float(company.exposures.get(s.id, 0.0))
        # horizon discount is deliberately mild; the exposure already represents
        # the cash-flow consequence at that horizon.
        horizon_weight = 1 / np.sqrt(max(s.horizon_years, 0.25))
        parts[s.id] = s.divergence * impact * horizon_weight
    raw = sum(parts.values())
    duration = 0.5 * company.cashflow_duration + 0.5 * company.technological_duration
    return raw * duration * company.evidence_confidence, parts


def composite_score(company: Company, scenarios: Iterable[Scenario],
                    obsolescence: float = 0.0, convergence: float = 0.0,
                    patentomics: float = 0.0,
                    weights: dict[str,float] | None = None) -> ScoreBreakdown:
    weights = weights or {"world":0.55, "obsolescence":0.20, "convergence":0.15, "patentomics":0.10}
    world, parts = world_divergence_score(company, scenarios)
    total = (weights["world"]*world - weights["obsolescence"]*obsolescence +
             weights["convergence"]*convergence + weights["patentomics"]*patentomics)
    return ScoreBreakdown(company.ticker, parts, world, obsolescence, convergence, patentomics, total)


def rank_companies(companies: list[Company], scenarios: list[Scenario],
                   aux: dict[str,dict[str,float]] | None = None) -> pd.DataFrame:
    rows=[]; aux=aux or {}
    for c in companies:
        a=aux.get(c.ticker,{})
        s=composite_score(c, scenarios, a.get("obsolescence",0), a.get("convergence",0), a.get("patentomics",0))
        rows.append({
            "ticker":c.ticker,"name":c.name,"sector":c.sector,
            "world_divergence":s.divergence_score,"obsolescence":s.obsolescence_score,
            "convergence":s.convergence_score,"patentomics":s.patentomics_score,
            "total_score":s.total_score,
            "direction":"beneficiary" if s.total_score>0 else "cashflow_at_risk",
        })
    return pd.DataFrame(rows).sort_values("total_score",ascending=False).reset_index(drop=True)
