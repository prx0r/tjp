"""Point-in-time observation store.

Every fact is an event with observed_at and effective_at.
Features can only use information available <= asof_ts.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Dict
import hashlib
import json
from dataclasses import dataclass


@dataclass
class ObservationFact:
    """Single factual observation with provenance."""
    observation_id: str
    project_id: str
    metric: str
    value: str
    observed_at: str
    effective_at: str
    source_url: str = ""
    source_type: str = ""
    content_hash: str = ""
    parser_version: str = ""
    confidence: str = "medium"


class ObservationStore:
    """Append-only store of factual observations. Never overwrites."""

    def __init__(self):
        self._facts: List[ObservationFact] = []
        self._index: Dict[str, List[int]] = {}  # project_id -> [indices]

    def add(self, fact: ObservationFact) -> None:
        idx = len(self._facts)
        self._facts.append(fact)
        self._index.setdefault(fact.project_id, []).append(idx)

    def query(self, project_id: str, metric: Optional[str] = None,
              asof_ts: Optional[str] = None) -> List[ObservationFact]:
        """Return facts for project, optionally filtered by metric and time.

        asof_ts: only return facts where effective_at <= asof_ts.
        """
        indices = self._index.get(project_id, [])
        results = []
        for idx in indices:
            f = self._facts[idx]
            if metric and f.metric != metric:
                continue
            if asof_ts and f.effective_at > asof_ts:
                continue
            results.append(f)
        return results

    def query_latest(self, project_id: str, metric: str) -> Optional[ObservationFact]:
        """Get latest fact for a metric, regardless of time."""
        indices = self._index.get(project_id, [])
        candidates = []
        for idx in indices:
            f = self._facts[idx]
            if f.metric == metric:
                candidates.append(f)
        if not candidates:
            return None
        return max(candidates, key=lambda f: f.effective_at)

    def verify_point_in_time(self, asof_ts: str) -> bool:
        """Assert no fact has effective_at > asof_ts (leakage check)."""
        for f in self._facts:
            if f.effective_at > asof_ts:
                return False
        return True

    def __len__(self):
        return len(self._facts)
