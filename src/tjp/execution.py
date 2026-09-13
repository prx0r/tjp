"""Depth-walking execution model for microcap market simulation.

Walks the ask side of an order book to determine actual fill prices.
Returns explicit execution quality classification.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class ExecutionQuality(str, Enum):
    EXACT_BOOK = "EXACT_BOOK"  # full book depth available
    TOP_OF_BOOK_ONLY = "TOP_OF_BOOK_ONLY"  # only top N levels visible
    TRADE_PROXY = "TRADE_PROXY"  # using trade history as approximation
    DAILY_PROXY = "DAILY_PROXY"  # using daily OHLCV only
    UNOBSERVABLE = "UNOBSERVABLE"  # insufficient data


@dataclass
class OrderLevel:
    price: float
    quantity: float  # base asset units


@dataclass
class ExecutionResult:
    requested_notional: float
    filled_notional: float
    fill_ratio: float
    base_quantity: float
    average_fill_price: float
    best_ask: float
    slippage_bps: float
    fee: float
    total_cost: float
    unfilled_notional: float
    levels_touched: int
    execution_quality: ExecutionQuality


def market_buy(
    asks: List[OrderLevel],
    quote_notional: float,
    fee_bps: float = 10.0,
    execution_quality: ExecutionQuality = ExecutionQuality.EXACT_BOOK,
) -> ExecutionResult:
    """Walk the ask side to simulate a market buy order.

    Args:
        asks: sorted list of ask levels (price ascending)
        quote_notional: USD amount to spend
        fee_bps: trading fee in basis points
        execution_quality: classification of data quality
    """
    if not asks:
        return ExecutionResult(
            requested_notional=quote_notional,
            filled_notional=0.0,
            fill_ratio=0.0,
            base_quantity=0.0,
            average_fill_price=0.0,
            best_ask=float('inf'),
            slippage_bps=0.0,
            fee=0.0,
            total_cost=quote_notional,
            unfilled_notional=quote_notional,
            levels_touched=0,
            execution_quality=execution_quality,
        )

    asks_sorted = sorted(asks, key=lambda x: x.price)
    best_ask = asks_sorted[0].price

    remaining = quote_notional
    base_filled = 0.0
    levels_touched = 0
    weighted_price_sum = 0.0

    for level in asks_sorted:
        if remaining <= 0:
            break
        quote_here = level.price * level.quantity
        take_quote = min(remaining, quote_here)
        base_take = take_quote / level.price

        weighted_price_sum += base_take * level.price
        base_filled += base_take
        remaining -= take_quote
        levels_touched += 1

    avg_fill = weighted_price_sum / base_filled if base_filled > 0 else 0.0
    slippage = ((avg_fill - best_ask) / best_ask * 10000) if best_ask > 0 else 0.0
    filled = quote_notional - remaining
    fee = filled * fee_bps / 10_000

    return ExecutionResult(
        requested_notional=quote_notional,
        filled_notional=filled,
        fill_ratio=filled / quote_notional if quote_notional > 0 else 0.0,
        base_quantity=base_filled,
        average_fill_price=round(avg_fill, 10),
        best_ask=best_ask,
        slippage_bps=round(slippage, 2),
        fee=fee,
        total_cost=filled + fee,
        unfilled_notional=remaining,
        levels_touched=levels_touched,
        execution_quality=execution_quality,
    )


def capacity_estimate(
    asks: List[OrderLevel],
    max_slippage_bps: float = 100.0,
    fee_bps: float = 10.0,
) -> dict:
    """Estimate how much capital can be deployed before exceeding slippage threshold."""
    if not asks:
        return {"max_notional": 0, "best_slippage": 0, "levels_used": 0}

    asks_sorted = sorted(asks, key=lambda x: x.price)
    best_ask = asks_sorted[0].price

    # Binary search for max capital at max_slippage
    lo, hi = 0.0, sum(l.price * l.quantity for l in asks_sorted) * 0.9
    best_capital = 0.0

    for _ in range(50):
        mid = (lo + hi) / 2
        if mid <= 0:
            break
        result = market_buy(asks_sorted, mid, 0.0, ExecutionQuality.EXACT_BOOK)
        if result.slippage_bps <= max_slippage_bps and result.fill_ratio >= 0.95:
            best_capital = mid
            lo = mid
        else:
            hi = mid

    final = market_buy(asks_sorted, best_capital, fee_bps, ExecutionQuality.EXACT_BOOK)
    return {
        "max_notional": round(best_capital, 2),
        "avg_slippage_bps": round(final.slippage_bps, 2),
        "levels_used": final.levels_touched,
        "avg_fill_price": final.average_fill_price,
    }
