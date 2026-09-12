"""Song Ma technological-obsolescence measure.

For firm f, horizon w and endpoint t:
  Base(f,t-w) = externally-owned patents cited by f up to t-w.
  Cit_tau(Base) = external citations made in year tau to that fixed base.
  Obsolescence^w_{f,t} = -[ln Cit_t(Base) - ln Cit_{t-w}(Base)].

Larger values mean a greater decline in usefulness of the firm's fixed
knowledge base. The paper tracks citations by firms other than f.
"""
from __future__ import annotations
import math
from collections import defaultdict
from typing import Iterable, Mapping


def technological_obsolescence(citations_start: float, citations_end: float, epsilon: float = 1e-9) -> float:
    if citations_start < 0 or citations_end < 0:
        raise ValueError("citation counts must be non-negative")
    return -(
        math.log(max(citations_end, epsilon)) -
        math.log(max(citations_start, epsilon))
    )


def construct_technology_base(
    firm: str,
    cutoff_year: int,
    backward_citations: Iterable[Mapping],
) -> set[str]:
    """Build fixed external technology base from citation-link records.

    Expected fields: citing_firm, citing_year, cited_patent, cited_owner.
    """
    base: set[str] = set()
    for r in backward_citations:
        if r["citing_firm"] != firm or int(r["citing_year"]) > cutoff_year:
            continue
        if r.get("cited_owner") == firm:
            continue
        base.add(str(r["cited_patent"]))
    return base


def external_citations_to_base(
    firm: str,
    year: int,
    technology_base: set[str],
    forward_citations: Iterable[Mapping],
) -> int:
    """Count citations in `year` to fixed base, excluding citations by firm."""
    return sum(
        1 for r in forward_citations
        if int(r["citing_year"]) == year
        and str(r["cited_patent"]) in technology_base
        and r.get("citing_firm") != firm
    )


def firm_obsolescence(
    firm: str,
    endpoint_year: int,
    horizon: int,
    backward_citations: Iterable[Mapping],
    forward_citations: Iterable[Mapping],
    min_base: int = 1,
) -> dict:
    start = endpoint_year - horizon
    base = construct_technology_base(firm, start, backward_citations)
    if len(base) < min_base:
        return {"firm": firm, "year": endpoint_year, "base_size": len(base), "obsolescence": None}
    c0 = external_citations_to_base(firm, start, base, forward_citations)
    c1 = external_citations_to_base(firm, endpoint_year, base, forward_citations)
    return {
        "firm": firm, "year": endpoint_year, "base_size": len(base),
        "citations_start": c0, "citations_end": c1,
        "obsolescence": technological_obsolescence(c0, c1),
    }
