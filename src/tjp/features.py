"""Point-in-time feature builder.

Features must only use information available <= asof_ts.
Never call "latest" APIs. Features are deterministic.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from .observations import ObservationStore


@dataclass
class PointInTimeFeatures:
    asof_ts: str
    project_id: str
    feature_version: str = "v1.0"

    # Exchange/discovery
    exchange_rank_at_t0: Optional[int] = None
    num_exchanges_at_t0: Optional[int] = None
    days_since_first_exchange: Optional[int] = None
    is_safetrade_first: Optional[bool] = None
    is_safetrade_first3: Optional[bool] = None

    # Age
    project_age_days: Optional[int] = None
    mainnet_age_days: Optional[int] = None
    repo_age_days: Optional[int] = None

    # GitHub
    commits_7d: Optional[int] = None
    commits_30d: Optional[int] = None
    contributors_30d: Optional[int] = None
    release_count_90d: Optional[int] = None

    # Infrastructure
    pool_count: Optional[int] = None
    miner_count: Optional[int] = None
    worker_count: Optional[int] = None
    hashrate: Optional[float] = None

    # Infrastructure velocity
    pool_count_delta_7d: Optional[int] = None
    miners_delta_7d: Optional[int] = None
    hashrate_delta_7d: Optional[float] = None

    # Tokenomics
    max_supply: Optional[float] = None
    circulating_supply: Optional[float] = None
    circulating_pct: Optional[float] = None
    premine_pct: Optional[float] = None
    team_pct: Optional[float] = None
    mineable_pct: Optional[float] = None

    # Market
    mcap_t0: Optional[float] = None
    fdv_t0: Optional[float] = None
    spread_bps: Optional[float] = None
    depth_1pct: Optional[float] = None
    volume_24h: Optional[float] = None

    # Technical taxonomy (deterministic, no LLM scores)
    pow: Optional[bool] = None
    useful_pow: Optional[bool] = None
    privacy: Optional[bool] = None
    post_quantum: Optional[bool] = None
    zk: Optional[bool] = None
    dag: Optional[bool] = None
    decentralized_compute: Optional[bool] = None
    ai_compute: Optional[bool] = None


def build_features(project_id: str, store: ObservationStore, asof_ts: str) -> PointInTimeFeatures:
    """Build features from point-in-time observation store."""
    feats = PointInTimeFeatures(asof_ts=asof_ts, project_id=project_id)

    # Helper to get latest value before asof
    def latest(metric: str, cast=None):
        obs = store.query_latest(project_id, metric)
        if obs is None or obs.effective_at > asof_ts:
            return None
        try:
            return cast(obs.value) if cast else obs.value
        except (ValueError, TypeError):
            return None

    feats.project_age_days = latest("project_age_days", int)
    feats.mainnet_age_days = latest("mainnet_age_days", int)
    feats.repo_age_days = latest("repo_age_days", int)
    feats.commits_30d = latest("commits_30d", int)
    feats.contributors_30d = latest("contributors_30d", int)
    feats.pool_count = latest("pool_count", int)
    feats.miner_count = latest("miner_count", int)
    feats.worker_count = latest("worker_count", int)
    feats.max_supply = latest("max_supply", float)
    feats.circulating_supply = latest("circulating_supply", float)
    feats.mcap_t0 = latest("mcap_t0", float)
    feats.volume_24h = latest("volume_24h", float)

    # Technical flags
    for flag in ["pow", "useful_pow", "privacy", "post_quantum", "zk", "dag",
                 "decentralized_compute", "ai_compute"]:
        setattr(feats, flag, latest(flag, lambda x: x.lower() == "true"))

    return feats
