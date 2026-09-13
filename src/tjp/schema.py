"""Event schemas — Pydantic models for listing events, observations, trades.

Every fact becomes an event with immutable ID, timestamps, and provenance.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class EventType(str, Enum):
    ANNOUNCED = "ANNOUNCED"
    MARKET_CREATED = "MARKET_CREATED"
    DEPOSITS_OPEN = "DEPOSITS_OPEN"
    ORDERBOOK_OPEN = "ORDERBOOK_OPEN"
    FIRST_BID = "FIRST_BID"
    FIRST_ASK = "FIRST_ASK"
    FIRST_TRADE = "FIRST_TRADE"
    WITHDRAWALS_OPEN = "WITHDRAWALS_OPEN"
    DELIST_ANNOUNCED = "DELIST_ANNOUNCED"
    MARKET_DISABLED = "MARKET_DISABLED"
    MIGRATED = "MIGRATED"
    RENAMED = "RENAMED"


class MarketState(str, Enum):
    ACTIVE = "ACTIVE"
    TEMP_DISABLED = "TEMP_DISABLED"
    RENAMED = "RENAMED"
    MIGRATED = "MIGRATED"
    DELISTED = "DELISTED"
    PROJECT_DEAD = "PROJECT_DEAD"
    EXCHANGE_DELISTED = "EXCHANGE_DELISTED"
    UNKNOWN = "UNKNOWN"


class ExecutionQuality(str, Enum):
    EXACT_BOOK = "EXACT_BOOK"
    TOP_OF_BOOK_ONLY = "TOP_OF_BOOK_ONLY"
    TRADE_PROXY = "TRADE_PROXY"
    DAILY_PROXY = "DAILY_PROXY"
    UNOBSERVABLE = "UNOBSERVABLE"


@dataclass
class ListingEvent:
    listing_event_id: str
    exchange_id: str
    project_id: str
    asset_id: str
    market_id: str
    event_type: EventType
    event_ts: str  # ISO UTC
    announcement_url: str = ""
    source_id: str = ""
    confidence: str = "medium"
    is_relist: bool = False
    is_migration: bool = False
    notes: str = ""


@dataclass
class TradeRecord:
    exchange_id: str
    market_id: str
    trade_id: str
    exchange_ts: str
    price: float  # will use Decimal in real impl
    quantity: float
    quote_quantity: float
    side: str
    sequence: int = 0
    source_id: str = ""


@dataclass
class OHLCVBar:
    market_id: str
    bar_size: str  # "1m", "5m", "1h", "1d"
    ts_open: str
    open: float
    high: float
    low: float
    close: float
    base_volume: float
    quote_volume: float
    trade_count: int
    vwap: float
    first_trade_ts: str = ""
    last_trade_ts: str = ""


@dataclass
class ObservationFact:
    observation_id: str
    project_id: str
    metric: str
    value: str  # flexible: string representation
    observed_at: str
    effective_at: str
    source_url: str
    source_type: str
    retrieved_at: str
    content_hash: str = ""
    parser_version: str = ""
    confidence: str = "medium"
