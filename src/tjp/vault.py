"""Vault stub: deposit / lock / withdraw, PAPER ONLY. 0 fee. No chain, no real funds.

Real-money path requires: audited contract + eligibility gates + human approval.
Until then every call records intent and returns paper state.
"""
from __future__ import annotations
from datetime import datetime, timezone

_ledger: list = []


def deposit(amount: float, currency: str = "USDG") -> dict:
    e = {"op": "deposit", "amount": amount, "currency": currency, "fee": 0.0, "mode": "paper",
         "ts": datetime.now(timezone.utc).isoformat()}
    _ledger.append(e)
    return e


def lock(amount: float, currency: str = "USDG") -> dict:
    e = {"op": "lock", "amount": amount, "currency": currency, "fee": 0.0, "mode": "paper",
         "ts": datetime.now(timezone.utc).isoformat()}
    _ledger.append(e)
    return e


def withdraw(amount: float, currency: str = "USDG") -> dict:
    e = {"op": "withdraw", "amount": amount, "currency": currency, "fee": 0.0, "mode": "paper",
         "ts": datetime.now(timezone.utc).isoformat()}
    _ledger.append(e)
    return e


def balance() -> dict:
    b = 0.0
    for e in _ledger:
        b += e["amount"] if e["op"] in ("deposit",) else (-e["amount"] if e["op"] == "withdraw" else 0.0)
    return {"paper_balance": round(b, 2), "ops": len(_ledger)}
