"""Canonical identity system — project_id, asset_id, market_id.

Ticker is an attribute, never an identifier. Events use immutable canonical IDs.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ProjectID:
    project_id: str  # canonical, e.g. "quantus", "pearl", "qubic"

    @classmethod
    def from_raw(cls, raw: str) -> "ProjectID":
        return cls(project_id=raw.lower().strip())

    def __str__(self) -> str:
        return self.project_id


@dataclass(frozen=True)
class AssetID:
    asset_id: str  # e.g. "quantus-mainnet-native", "pearl-mainnet"
    project_id: str
    network: str

    def __str__(self) -> str:
        return self.asset_id


@dataclass(frozen=True)
class MarketID:
    market_id: str  # e.g. "safetrade:quantus:usdt"
    exchange_id: str
    asset_id: str
    quote_asset: str = "usdt"

    def __str__(self) -> str:
        return self.market_id


@dataclass(frozen=True)
class SymbolRecord:
    """Temporal symbol: ticker changes over time on a given venue."""
    asset_id: str
    venue: str
    symbol: str
    valid_from: str  # ISO timestamp
    valid_to: Optional[str] = None  # None = current
    source_id: str = ""


# Known renames / migrations
RENAME_LOG = [
    {
        "project": "quantus",
        "old_symbol": "QUAN",
        "new_symbol": "QUANTUS",
        "venue": "safetrade",
        "change_date": "2026-09-11",
        "reason": "ticker renamed for consistency",
        "market_old": "quanusdt",
        "market_new": "quantususdt",
    },
    {
        "project": "pearl",
        "old_symbol": "PRL",
        "new_symbol": "PEARL",
        "venue": "safetrade",
        "change_date": None,  # metadata mismatch only
        "reason": "listing metadata shows PEARL/USDT; actual markets use PRL",
        "market_old": None,
        "market_new": None,
    },
]

# Canonical mapping: SafeTrade asset names → project_id
SAFE_ASSET_MAP = {
    "QUAN": "quantus",
    "QUANTUS": "quantus",
    "PRL": "pearl",
    "PEARL": "pearl",
    "TSC": "tensorcash",
    "NOID": "paranoid",
    "CNX": "crynux",
    "MDL": "modelos",
    "CSD": "computesubstrate",
    "KRGN": "kerrigan",
    "SNAP": "snap",
    "CPAY": "cryptix",
    "VE": "vecno",
    "GNK": "gonka",
    "LAX": "parallax",
    "VRL": "virel",
    "QTC": "qubitcoin",
    "NOCK": "nockchain",
    "XTM": "tari",
    "XEL": "xel",
    "WART": "wart",
    "XMR": "monero",
    "BTC": "bitcoin",
    "ETH": "ethereum",
}


def resolve_project(safe_asset: str) -> Optional[str]:
    """Resolve SafeTrade asset name to canonical project_id."""
    return SAFE_ASSET_MAP.get(safe_asset.upper())


def make_market_id(exchange: str, base: str, quote: str = "usdt") -> str:
    return f"{exchange}:{base.lower()}:{quote.lower()}"
