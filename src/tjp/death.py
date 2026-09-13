"""Death Token Strategy v2 — structural decay + supply pressure analysis.

Mirror image of SafeTrade long study. Measures Death Pressure Ratio,
shortability, and forward decay. THEORETICAL_SHORT vs EXECUTABLE_SHORT.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class DeathCategory(str, Enum):
    THEORETICAL = "THEORETICAL_DEATH"  # price eventually collapsed
    SHORTABLE = "SHORTABLE_DEATH"  # borrow/perp available
    EXECUTABLE = "EXECUTABLE_DEATH"  # depth allowed our size
    SURVIVABLE = "SURVIVABLE_DEATH"  # MAE within risk threshold


class DeathStrategy(str, Enum):
    ALL = "DEATH_ALL"  # short every new listing
    ONE_DAY = "DEATH_1D"  # short after +24h pump
    SEVEN_DAY = "DEATH_7D"  # short at +7d
    FADE = "DEATH_FADE"  # wait for volume peak + 50% decline
    SUPPLY = "DEATH_SUPPLY"  # short when DPR > threshold
    FDV = "DEATH_FDV"  # short when FDV/float > threshold
    MINER = "DEATH_MINER"  # short when emission/spot > threshold
    COMBINED = "DEATH_COMBINED"  # multiple bearish signals


@dataclass
class SupplyPressure:
    """Structural supply-side analysis for a microcap project."""
    project_id: str
    ts: str  # analysis timestamp, ISO

    # Emission
    daily_issued_usd: float  # E_m: new miner emission in USD/day
    daily_unlock_usd: float  # E_u: unlock-related expected sellable issuance
    daily_inflation_usd: float  # E_i: other inflationary issuance

    # Demand / liquidity
    daily_spot_volume_usd: float  # V_o
    liquidity_depth_usd: float  # L_q: 1-5% depth in USD

    # Derived
    death_pressure_ratio: float  # DPR = (E_m + E_u + E_i) / (V_o * L_q)
    emission_rate: float  # daily emission / circulating supply
    miner_share: float  # miner daily revenue / daily volume


@dataclass
class ShortMetrics:
    """Execution feasibility of a short position."""
    project_id: str
    ts: str

    borrow_available: bool
    borrow_apr: Optional[float] = None
    perp_available: bool = False
    funding_rate: Optional[float] = None
    depth_1pct_usd: float = 0.0
    depth_5pct_usd: float = 0.0
    venue_count: int = 0
    max_shortable_notional: float = 0.0


@dataclass
class DeathEventStudy:
    """Forward return and decay analysis for one listing."""
    listing_event_id: str
    project_id: str
    exchange_id: str

    # Raw decay returns
    return_1d: Optional[float] = None
    return_7d: Optional[float] = None
    return_30d: Optional[float] = None
    return_90d: Optional[float] = None

    # Short-side MFE (max adverse excursion for the SHORT)
    max_price_after_entry: float = 0.0
    peak_upside_pct: float = 0.0  # MAE for short: max(P_t/P_0 - 1)
    time_to_peak_days: Optional[int] = None

    # Monetization
    max_subsequent_decline_pct: float = 0.0
    time_to_25pct_decline: Optional[int] = None
    time_to_50pct_decline: Optional[int] = None
    time_to_75pct_decline: Optional[int] = None
    time_to_90pct_decline: Optional[int] = None

    # Structural
    death_pressure_ratio: Optional[float] = None
    fdv_float_ratio: Optional[float] = None
    emission_rate: Optional[float] = None

    # Shortability
    volume_at_entry: float = 0.0
    depth_at_entry: float = 0.0
    borrow_available: bool = False
    borrow_apr: Optional[float] = None
    perp_available: bool = False
    venue_count: int = 0

    # Classification
    death_category: Optional[DeathCategory] = None


@dataclass
class DeathResult:
    """Outcome of one death strategy on one listing."""
    strategy: DeathStrategy
    listing_event_id: str
    project_id: str

    # Entry
    entry_ts: str
    entry_price: float
    entry_notional: float
    execution_quality: str  # THEORETICAL / SHORTABLE / EXECUTABLE / SURVIVABLE

    # Forward returns (SHORT perspective: positive = price fell)
    return_1d: Optional[float] = None
    return_7d: Optional[float] = None
    return_30d: Optional[float] = None
    return_90d: Optional[float] = None

    # Risk: max adverse excursion (for short, this is price going UP)
    max_adverse_excursion: float = 0.0
    survived_risk: bool = False  # MAE exceeded threshold

    # Decay
    peak_decline_pct: float = 0.0  # max price drop after entry
    days_to_50pct_decline: Optional[int] = None
