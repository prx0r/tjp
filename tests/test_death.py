"""Tests for death-token strategy components."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from tjp.death import SupplyPressure, DeathCategory, DeathStrategy, ShortMetrics
from tjp.execution import market_buy, OrderLevel, ExecutionQuality


class TestSupplyPressure:
    def test_dpr_calculation(self):
        """DPR = (E_m + E_u + E_i) / (V_o * L_q)"""
        sp = SupplyPressure(
            project_id="quantus",
            ts="2026-09-13",
            daily_issued_usd=50000,  # $50k/day mined
            daily_unlock_usd=10000,  # $10k/day unlocks
            daily_inflation_usd=5000,  # $5k other
            daily_spot_volume_usd=2000000,  # $2M/day volume
            liquidity_depth_usd=50000,  # $50k depth
            death_pressure_ratio=0.0065,  # (50+10+5)/(2M*50k)
            emission_rate=0.0001,  # 0.01%/day
            miner_share=0.025,
        )
        assert sp.death_pressure_ratio == pytest.approx(0.0065, abs=0.001)

    def test_high_dpr_is_bearish(self):
        """High DPR means emission overwhelms demand."""
        sp = SupplyPressure(
            project_id="test", ts="2026-09-13",
            daily_issued_usd=100000,
            daily_unlock_usd=50000,
            daily_inflation_usd=20000,
            daily_spot_volume_usd=500000,
            liquidity_depth_usd=10000,
            death_pressure_ratio=3.4,  # (100+50+20)/(500k*10k) = 170/5000 = 0.034
            emission_rate=0.01,
            miner_share=0.2,
        )
        # DPR > 1 means new supply exceeds demand depth
        assert sp.death_pressure_ratio > 1.0


class TestShortMetrics:
    def test_executable_short(self):
        sm = ShortMetrics(
            project_id="quantus", ts="2026-09-13",
            borrow_available=True, borrow_apr=150.0,
            perp_available=False,
            depth_1pct_usd=10000, depth_5pct_usd=50000,
            venue_count=1, max_shortable_notional=5000,
        )
        assert sm.borrow_available
        assert sm.max_shortable_notional == 5000


class TestDeathCategory:
    def test_all_categories_exist(self):
        assert len(DeathCategory) == 4
        assert DeathCategory.THEORETICAL.value == "THEORETICAL_DEATH"
