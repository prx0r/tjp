"""Tests for normalized trades, observations, features, event study, portfolio."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from datetime import datetime, timezone
from tjp.normalize import normalize_trade, normalize_timestamp, deduplicate_trades, NormalizedTrade
from tjp.observations import ObservationStore, ObservationFact
from tjp.features import build_features, PointInTimeFeatures
from tjp.event_study import TimestampedPrice, price_at_horizon, event_study_entry, HORIZONS_UTC
from tjp.portfolio import Portfolio


class TestNormalizedTrades:
    def test_timestamp_rejects_naive(self):
        with pytest.raises(ValueError, match="Naive timestamp"):
            normalize_timestamp("2026-05-23 12:00:00")

    def test_timestamp_normalizes_utc(self):
        assert normalize_timestamp("2026-05-23T12:00:00+02:00") == "2026-05-23T12:00:00+02:00"
        assert normalize_timestamp("2026-05-23T12:00:00") == "2026-05-23T12:00:00Z"

    def test_price_decimal_precision(self):
        t = normalize_trade("x", "x:btc:usdt", "t1", "btc", "btc-main", 0.000000001, 100, 0.0001, "buy", "2026-05-23T12:00:00Z")
        assert "0.000000001" in t.price

    def test_dedup(self):
        t1 = normalize_trade("x", "x:btc:usdt", "t1", "btc", "btc-main", 1.0, 10, 10.0, "buy", "2026-05-23T12:00:00Z")
        t2 = normalize_trade("x", "x:btc:usdt", "t1", "btc", "btc-main", 1.0, 10, 10.0, "buy", "2026-05-23T12:00:00Z")
        result = deduplicate_trades([t1, t2])
        assert len(result) == 1


class TestObservations:
    def test_point_in_time_query(self):
        store = ObservationStore()
        store.add(ObservationFact("o1", "quantus", "pool_count", "6", "2026-09-10", "2026-09-09", "", "", "", "", "1.0"))
        store.add(ObservationFact("o2", "quantus", "pool_count", "8", "2026-09-12", "2026-09-11", "", "", "", "", "1.0"))
        # Query at Sep 10 should only see pool_count=6
        results = store.query("quantus", "pool_count", "2026-09-10T23:59:59Z")
        assert len(results) == 1
        assert results[0].value == "6"

    def test_leakage_detection(self):
        store = ObservationStore()
        store.add(ObservationFact("o1", "quantus", "pool_count", "6", "2026-09-10", "2026-09-09", "", "", "", "", "1.0"))
        store.add(ObservationFact("o2", "quantus", "pool_count", "8", "2026-09-12", "2026-09-11", "", "", "", "", "1.0"))
        assert not store.verify_point_in_time("2026-09-10T00:00:00Z")


class TestFeatures:
    def test_empty_store_returns_nulls(self):
        store = ObservationStore()
        feats = build_features("quantus", store, "2026-09-10T00:00:00Z")
        assert feats.pool_count is None
        assert feats.mcap_t0 is None
        assert feats.pow is None


class TestEventStudy:
    def test_price_at_horizon(self):
        prices = [
            TimestampedPrice(ts=datetime(2026, 5, 23, tzinfo=timezone.utc), price=1.0),
            TimestampedPrice(ts=datetime(2026, 5, 24, tzinfo=timezone.utc), price=1.5),
            TimestampedPrice(ts=datetime(2026, 5, 30, tzinfo=timezone.utc), price=2.0),
        ]
        entry = TimestampedPrice(ts=datetime(2026, 5, 23, tzinfo=timezone.utc), price=1.0)
        assert price_at_horizon(entry, prices, 86400) == 1.5  # +1d
        assert price_at_horizon(entry, prices, 7 * 86400) == 2.0  # +7d
        assert price_at_horizon(entry, prices, 365 * 86400) is None  # beyond data

    def test_event_study_returns_excess(self):
        listing = TimestampedPrice(ts=datetime(2026, 5, 23, tzinfo=timezone.utc), price=1.0)
        asset = [
            TimestampedPrice(ts=datetime(2026, 5, 23, tzinfo=timezone.utc), price=1.0),
            TimestampedPrice(ts=datetime(2026, 5, 24, tzinfo=timezone.utc), price=2.0),
        ]
        btc = [
            TimestampedPrice(ts=datetime(2026, 5, 23, tzinfo=timezone.utc), price=100000),
            TimestampedPrice(ts=datetime(2026, 5, 24, tzinfo=timezone.utc), price=105000),
        ]
        eth = btc.copy()
        result = event_study_entry(listing.ts, asset, btc, eth)
        assert result["returns"]["24h"] == pytest.approx(1.0)  # 2x in 24h
        assert result["benchmark_returns"]["btc_24h"] == pytest.approx(0.05)


class TestPortfolio:
    def test_cash_accounting(self):
        p = Portfolio(initial_cash=10000, allocation_per_listing=1000, fee_bps=200)
        assert p.can_buy()
        p.buy("quantus", 50.0, "2026-09-13")
        assert p.cash == 9000.0
        # investable = 1000 - 20 = 980; qty = 980/50 = 19.6 units
        assert p.position_value("quantus", 50.0) == pytest.approx(980.0)
        summary = p.summary({"quantus": 50.0})
        assert summary["total_value"] == pytest.approx(9980.0)
        assert summary["return_pct"] == pytest.approx(-0.2, abs=0.01)

    def test_insufficient_cash(self):
        p = Portfolio(initial_cash=500, allocation_per_listing=1000)
        assert not p.can_buy()
        result = p.buy("quantus", 50.0, "2026-09-13")
        assert not result
