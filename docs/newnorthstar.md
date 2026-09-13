# TJP / SafeTrade quantitative research rebuild — newnorthstar.md

Saved from message 2026-09-13.

## Objective

Turn the current SafeTrade research prototype into a reproducible, point-in-time quantitative research system.

data integrity → event model → execution model → outcomes → portfolio backtest → features → ML.

## Key insight

Use SafeTrade to learn the precursor graph (pool creation, miner integrations, repo acceleration, independent infrastructure, OTC emergence, first obscure venue) and attempt to identify Quantus/Pearl/Qubic-like projects at D1–D4 instead of D5. That is potentially much more valuable than the buy-at-listing strategy.

## Core rule

immutable observation → canonical identity → point-in-time feature → explicit event → executable trade assumption → deterministic outcome.

## Most important: do not optimize for generating a result. Optimize for making it difficult to accidentally lie to ourselves.

## 10 immediate fixes

1. Delete sim.py startswith(asset) market resolution.
2. Stop calling disabled markets "dead."
3. Fix PRL identity (PEARL/USDT vs PRL).
4. Kill observation-index horizons.
5. Kill fake Sharpe and win rate.
6. Fix buy_hold capital accounting.
7. Stop charging exit fee to canonical "never sell."
8. Don't plot fill number as time.
9. Replace always-pass tests.
10. Get raw data out of docs/.

## V1 definition of done

Run: tjp research build safetrade-v1 → outputs: listing_events.parquet, t0_features.parquet, outcomes.parquet, safe_all.parquet, reports.
Then: tjp research verify safetrade-v1 → detects lookahead, unknown identities, duplicates, future features, impossible fills, timestamp violations.
