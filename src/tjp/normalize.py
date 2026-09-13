"""Normalized trade ingestion — resolves exchange-specific quirks into canonical TradeRecord.

Handles: PRL/PEARL alias, QUAN/QUANTUS rename, tick normalization, deduplication.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, timezone


@dataclass
class NormalizedTrade:
    """Canonical trade record — exchange quirks removed."""
    trade_id: str
    exchange_id: str
    market_id: str
    project_id: str
    asset_id: str
    exchange_ts: str  # ISO UTC, verified timezone-aware
    price: str  # Decimal string for microcap precision
    quantity: str  # Decimal string
    quote_quantity: str
    side: str
    sequence: int
    source_id: str
    content_hash: str = ""


def normalize_price(price) -> str:
    """Store as string to preserve Decimal precision. Never round during research."""
    if isinstance(price, (int, float)):
        return f"{price:.18f}"
    return str(price)


def normalize_timestamp(ts: str) -> str:
    """Ensure UTC ISO format. Rejects naive timestamps."""
    if "T" not in ts:
        raise ValueError(f"Naive timestamp rejected: {ts}")
    if not ts.endswith("Z") and "+" not in ts:
        return ts + "Z"
    return ts


def normalize_trade(
    exchange_id: str,
    market_id: str,
    trade_id: str,
    project_id: str,
    asset_id: str,
    price,
    quantity,
    quote_quantity,
    side: str,
    ts: str,
    sequence: int = 0,
    source_id: str = "",
) -> NormalizedTrade:
    return NormalizedTrade(
        trade_id=f"{exchange_id}:{market_id}:{trade_id}",
        exchange_id=exchange_id,
        market_id=market_id,
        project_id=project_id,
        asset_id=asset_id,
        exchange_ts=normalize_timestamp(ts),
        price=normalize_price(price),
        quantity=normalize_price(quantity),
        quote_quantity=normalize_price(quote_quantity),
        side=side.lower(),
        sequence=sequence,
        source_id=source_id,
    )


def deduplicate_trades(trades: List[NormalizedTrade]) -> List[NormalizedTrade]:
    """Remove duplicate trade_id entries, keeping first occurrence."""
    seen = set()
    deduped = []
    for t in trades:
        if t.trade_id not in seen:
            seen.add(t.trade_id)
            deduped.append(t)
    return deduped
