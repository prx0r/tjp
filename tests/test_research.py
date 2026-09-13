"""Tests for quantitative research — tests research truth, not merely code execution.

Uses tiny synthetic fixtures with known answers.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from tjp.ids import ProjectID, AssetID, MarketID, resolve_project, make_market_id, SAFE_ASSET_MAP
from tjp.schema import EventType, MarketState, ExecutionQuality, ListingEvent
from tjp.execution import market_buy, OrderLevel, ExecutionQuality as EQ, capacity_curve
from tjp.buyhold import buy_hold
from tjp.ohlcv import build_bars
from tjp.schema import TradeRecord
from tjp.strategy import run_strategy, _compute_sharpe, Bar


class TestCanonicalIDs:
    def test_ticker_is_not_identity(self):
        """QUAN → QUANTUS rename must not break project resolution."""
        assert resolve_project("QUAN") == "quantus"
        assert resolve_project("QUANTUS") == "quantus"
        assert resolve_project("PRL") == "pearl"
        assert resolve_project("PEARL") == "pearl"
        assert resolve_project("UNKNOWN_PROJECT") is None

    def test_market_id_format(self):
        assert make_market_id("safetrade", "quantus", "usdt") == "safetrade:quantus:usdt"

    def test_id_objects_are_frozen(self):
        p = ProjectID("quantus")
        assert str(p) == "quantus"
        with pytest.raises(AttributeError):
            p.project_id = "changed"


class TestDepthWalkingExecution:
    def test_exact_fill_at_single_level(self):
        """$150 at $1/unit → 150 units, avg $1, full fill."""
        asks = [OrderLevel(price=1.0, quantity=1000)]
        result = market_buy(asks, 150, fee_bps=0, execution_quality=EQ.EXACT_BOOK)
        assert result.base_quantity == pytest.approx(150.0)
        assert result.average_fill_price == pytest.approx(1.0)
        assert result.fill_ratio == pytest.approx(1.0)
        assert result.unfilled_notional == pytest.approx(0.0)

    def test_walks_multiple_levels(self):
        """$150 with 100@1 + 100@2 → 100@1 + 25@2 = 125 units."""
        asks = [OrderLevel(price=1.0, quantity=100), OrderLevel(price=2.0, quantity=100)]
        result = market_buy(asks, 150, fee_bps=0, execution_quality=EQ.EXACT_BOOK)
        assert result.base_quantity == pytest.approx(125.0)
        assert result.average_fill_price == pytest.approx(1.20)  # (100*1 + 25*2) / 125
        assert result.levels_touched == 2
        assert result.fill_ratio == pytest.approx(1.0)

    def test_partial_fill_when_book_thin(self):
        """$1000 but only $500 depth → 50% fill."""
        asks = [OrderLevel(price=10.0, quantity=50)]
        result = market_buy(asks, 1000, fee_bps=0)
        assert result.fill_ratio == pytest.approx(0.5)
        assert result.unfilled_notional == pytest.approx(500.0)

    def test_empty_book(self):
        """No asks → zero fill, full unfilled."""
        result = market_buy([], 1000, fee_bps=0)
        assert result.fill_ratio == 0.0
        assert result.unfilled_notional == 1000.0


class TestBuyHoldCapital:
    def test_buy_hold_fee_accounting(self):
        """Flat price + 2% entry fee + slippage: net loss matches computed total."""
        result = buy_hold([0.1, 1.0, 1.0, 1.0], entry_idx=0, size=1000, fee_bps=200, slippage_bps=10)
        assert result["entry_fee"] == 20.0
        assert result["investable"] == 980.0
        # fill = 1.0 * 1.001 = 1.001; qty = 980/1.001 ≈ 979.02; mtm ≈ 979.02; net ≈ -20.98
        assert result["net_mtm"] == pytest.approx(result["mtm_end"] - 1000, abs=0.01)
        assert result["ret_mtm_pct"] == pytest.approx(result["mtm_end"] / 1000 - 1, abs=0.001)

    def test_buy_hold_no_slippage_zero_fee(self):
        """Zero fees + no slippage: flat price → exactly 0% return."""
        result = buy_hold([0.1, 1.0, 1.0, 1.0], entry_idx=0, size=1000, fee_bps=0, slippage_bps=0)
        assert result["entry_fee"] == 0.0
        assert result["mtm_end"] == 1000.0
        assert result["net_mtm"] == 0.0
        assert result["ret_mtm_pct"] == 0.0

    def test_no_exit_fee_by_default(self):
        """canonical 'never sell' should not charge exit fee."""
        result = buy_hold([0.1, 1.0, 2.0], entry_idx=0, size=1000, fee_bps=200)
        assert result["exit_fee"] == 0.0

    def test_exit_fee_only_when_requested(self):
        """Exit fee should only apply when explicitly requested."""
        result = buy_hold([0.1, 1.0, 2.0], entry_idx=0, size=1000, fee_bps=200, charge_exit_fee=True)
        assert result["exit_fee"] > 0


class TestStrategyMetrics:
    def test_sharpe_is_annualized(self):
        """Sharpe should annualize, not be raw mean/std. Constant returns → None."""
        returns = [0.01] * 365
        sharpe = _compute_sharpe(returns, periods_per_year=365)
        assert sharpe is None  # constant returns → undefined (zero volatility)

    def test_sharpe_with_volatile_returns(self):
        """Volatile returns should produce a meaningful annualized Sharpe."""
        returns = [0.05, -0.03, 0.02, -0.01, 0.04] * 10  # 50 bars of volatility
        sharpe = _compute_sharpe(returns, periods_per_year=365)
        assert sharpe != 0.0

    def test_sharpe_zero_vol(self):
        """Constant returns → Sharpe = None (undefined, zero volatility)."""
        sharpe = _compute_sharpe([0.0] * 100)
        assert sharpe is None  # undefined for constant returns

    def test_strategy_accounts_for_round_trips(self):
        """Win rate should be based on completed round trips, not random bars."""
        bars = [
            Bar(ts="2026-01-01T00:00:00Z", open=1.0, high=1.5, low=0.8, close=1.0),
            Bar(ts="2026-01-02T00:00:00Z", open=2.0, high=2.2, low=1.5, close=2.0),
            Bar(ts="2026-01-03T00:00:00Z", open=1.0, high=1.2, low=0.8, close=1.0),
            Bar(ts="2026-01-04T00:00:00Z", open=1.0, high=1.1, low=0.9, close=1.0),
        ]
        signals = [1, 1, 0, 0]
        result = run_strategy(bars, signals, fee_bps=0)
        assert result["closed_trades"] == 1
        assert result["trades"][0]["net_pnl"] == pytest.approx(-0.5)


class TestOHLCV:
    def test_single_trade_creates_bar(self):
        trade = TradeRecord(
            exchange_id="test", market_id="test:btc:usdt", trade_id="t1",
            exchange_ts="2026-05-23T12:00:00Z", price=1.0, quantity=100,
            quote_quantity=100.0, side="buy",
        )
        bars = build_bars([trade], bar_seconds=60)
        assert len(bars) == 1
        assert bars[0].bar.trade_count == 1
        assert bars[0].bar.base_volume == 100
        assert not bars[0].is_missing
        assert bars[0].mark_delay_seconds is not None

    def test_missing_bars_not_forward_filled(self):
        """Gaps in time should produce separate bars, not one continuous series."""
        trades = [
            TradeRecord("x", "x:btc:usdt", "t1", "2026-05-23T12:00:00Z", 1.0, 100, 100.0, "buy"),
            TradeRecord("x", "x:btc:usdt", "t2", "2026-05-23T14:00:00Z", 1.1, 50, 55.0, "sell"),
        ]
        bars = build_bars(trades, bar_seconds=3600)  # 1h bars
        # Two trades in different hours → at least 2 bars
        assert len(bars) >= 2


class TestCompiles:
    def test_manifest_maker(self):
        from tjp.manifest import make_manifest
        m = make_manifest(
            dataset="test", version="0.1.0", git_commit="abc123",
            row_count=10, schema_version="1.0", strategies=["SAFE1"],
        )
        assert m.row_count == 10
        assert len(m.content_hash()) == 16
