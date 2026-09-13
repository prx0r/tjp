"""Portfolio backtest engine.

Handles: cash accounting, fixed allocation, mark-to-market, capacity.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime, timezone


@dataclass
class Position:
    project_id: str
    entry_ts: str
    entry_price: float
    quantity: float
    cost_basis: float  # total USD spent including fees


@dataclass
class CashFlow:
    ts: str
    amount: float  # positive = cash in, negative = cash out
    reason: str


class Portfolio:
    """Fixed-capital portfolio with cash accounting."""

    def __init__(self, initial_cash: float, allocation_per_listing: float = 1000.0,
                 fee_bps: float = 20.0):
        self.initial_cash = initial_cash
        self.allocation = allocation_per_listing
        self.fee_bps = fee_bps
        self.cash = initial_cash
        self.positions: Dict[str, Position] = {}
        self.cash_flows: List[CashFlow] = []
        self.trade_log: List[dict] = []

    def can_buy(self) -> bool:
        return self.cash >= self.allocation

    def buy(self, project_id: str, price: float, ts: str) -> bool:
        """Buy allocation worth. Returns False if insufficient cash."""
        if self.cash < self.allocation:
            return False
        fee = self.allocation * self.fee_bps / 10_000
        investable = self.allocation - fee
        qty = investable / price
        self.cash -= self.allocation
        self.cash_flows.append(CashFlow(ts=ts, amount=-self.allocation, reason="buy"))
        self.positions[project_id] = Position(
            project_id=project_id, entry_ts=ts, entry_price=price,
            quantity=qty, cost_basis=self.allocation,
        )
        self.trade_log.append({
            "project": project_id, "action": "buy", "price": price,
            "quantity": qty, "cost": self.allocation, "ts": ts,
        })
        return True

    def mark_to_market(self, prices: Dict[str, float]) -> float:
        """Total portfolio value = cash + sum(position_value)."""
        pos_value = sum(p.quantity * prices.get(p.project_id, p.entry_price)
                       for p in self.positions.values())
        return self.cash + pos_value

    def position_value(self, project_id: str, price: float) -> float:
        p = self.positions.get(project_id)
        return p.quantity * price if p else 0.0

    def summary(self, prices: Dict[str, float]) -> dict:
        total = self.mark_to_market(prices)
        invested = sum(p.cost_basis for p in self.positions.values())
        return {
            "cash": round(self.cash, 2),
            "positions": len(self.positions),
            "total_value": round(total, 2),
            "invested": round(invested, 2),
            "return_pct": round((total / self.initial_cash - 1) * 100, 4),
            "num_buys": len([f for f in self.cash_flows if f.amount < 0]),
        }
