"""Depth-walking execution model for microcap market simulation.

Walks the order book for spot BUY and SELL.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List
from enum import Enum


class ExecutionQuality(str, Enum):
    EXACT_BOOK = "EXACT_BOOK"
    TOP_OF_BOOK_ONLY = "TOP_OF_BOOK_ONLY"
    TRADE_PROXY = "TRADE_PROXY"
    DAILY_PROXY = "DAILY_PROXY"
    UNOBSERVABLE = "UNOBSERVABLE"


@dataclass
class OrderLevel:
    price: float
    quantity: float


@dataclass
class ExecutionResult:
    requested_notional: float
    filled_notional: float
    fill_ratio: float
    base_quantity: float
    average_fill_price: float
    best_price: float
    slippage_bps: float
    fee: float
    total_cost: float  # filled + fee; always <= requested_notional
    unfilled_notional: float
    levels_touched: int
    execution_quality: ExecutionQuality
    side: str


def market_buy(book: List[OrderLevel], cash_budget: float,
               fee_bps: float = 10.0, execution_quality: ExecutionQuality = ExecutionQuality.EXACT_BOOK) -> ExecutionResult:
    """Cash budget INCLUDES fees. Total cost <= cash_budget always."""
    if not book:
        return ExecutionResult(
            requested_notional=cash_budget, filled_notional=0.0, fill_ratio=0.0,
            base_quantity=0.0, average_fill_price=0.0, best_price=0.0,
            slippage_bps=0.0, fee=0.0, total_cost=0.0, unfilled_notional=cash_budget,
            levels_touched=0, execution_quality=execution_quality, side="buy",
        )
    asks = sorted(book, key=lambda x: x.price)
    best = asks[0].price
    rate = fee_bps / 10_000
    tradable = cash_budget / (1 + rate)
    remaining = tradable
    base_filled = 0.0
    weighted = 0.0
    levels = 0

    for level in asks:
        if remaining <= 0:
            break
        avail_quote = level.price * level.quantity
        take = min(remaining, avail_quote)
        base_take = take / level.price
        weighted += base_take * level.price
        base_filled += base_take
        remaining -= take
        levels += 1

    avg_fill = weighted / base_filled if base_filled > 0 else 0.0
    slippage = ((avg_fill - best) / best * 10_000) if best > 0 else 0.0
    filled = tradable - remaining
    fee = filled * rate
    total = filled + fee
    assert total <= cash_budget + 1e-9, "Invariant: total_cost <= cash_budget"

    return ExecutionResult(
        requested_notional=cash_budget, filled_notional=filled,
        fill_ratio=filled / cash_budget if cash_budget > 0 else 0.0,
        base_quantity=base_filled, average_fill_price=round(avg_fill, 10),
        best_price=best, slippage_bps=round(slippage, 2),
        fee=round(fee, 6), total_cost=round(total, 6),
        unfilled_notional=cash_budget - total, levels_touched=levels,
        execution_quality=execution_quality, side="buy",
    )


def market_sell(book: List[OrderLevel], base_quantity: float,
                fee_bps: float = 10.0, execution_quality: ExecutionQuality = ExecutionQuality.EXACT_BOOK) -> ExecutionResult:
    """Walk bid side to sell base_quantity. Sells into the best available bids."""
    if not book:
        return ExecutionResult(
            requested_notional=0.0, filled_notional=0.0, fill_ratio=0.0,
            base_quantity=base_quantity, average_fill_price=0.0, best_price=0.0,
            slippage_bps=0.0, fee=0.0, total_cost=0.0,
            unfilled_notional=0.0, levels_touched=0, execution_quality=execution_quality, side="sell",
        )
    bids = sorted(book, key=lambda x: x.price, reverse=True)
    best = bids[0].price
    remaining = base_quantity
    quote_filled = 0.0
    levels = 0
    for level in bids:
        if remaining <= 0:
            break
        take_base = min(remaining, level.quantity)
        quote_filled += take_base * level.price
        remaining -= take_base
        levels += 1
    avg = quote_filled / (base_quantity - remaining) if base_quantity - remaining > 0 else 0.0
    fee = quote_filled * fee_bps / 10_000
    unfilled = remaining * best if best > 0 else 0.0
    slippage = ((best - avg) / best * 10_000) if best > 0 else 0.0

    return ExecutionResult(
        requested_notional=quote_filled + fee, filled_notional=quote_filled,
        fill_ratio=(base_quantity - remaining) / base_quantity if base_quantity > 0 else 0.0,
        base_quantity=base_quantity - remaining, average_fill_price=avg,
        best_price=best, slippage_bps=slippage, fee=fee,
        total_cost=fee, unfilled_notional=unfilled,
        levels_touched=levels, execution_quality=execution_quality, side="sell",
    )


def capacity_curve(book: List[OrderLevel], notional_steps: List[float], fee_bps: float = 10.0):
    """For each notional step, compute actual execution quality and slippage."""
    return [
        {
            "notional": n,
            "result": market_buy(book, n, fee_bps),
        }
        for n in sorted(notional_steps)
    ]
