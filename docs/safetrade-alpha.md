# SafeTrade experiment — Frontier Crypto Index (2026-09-13, saved word for word)

## Two strategies: SafeTrade index + discovery venue ranking

### Strategy 1: SafeTrade Index
SafeTrade has a genuine niche as early venue for strange, technically ambitious, low-cap infrastructure coins. Testing whether a SafeTrade listing acts as early-stage technical-crypto discovery signal.

SAFE1: listing-day equal weight (buy $100 first executable price, never sell).
SAFE2: Frontier basket (novel PoW, useful PoW, privacy, PQ, ZK, compute).
SAFE3: Tom filter (mineable + novel + <$100m + native chain + GitHub).

Measure: 1d/7d/30d/90d/180d/365d/current return, max drawdown, max gain, days to ATH, daily volume, mcap at entry, SafeTrade liquidity, later CEX listings, survival/dead/delisted, BTC-relative return.

### Strategy 2: Discovery venue ranking
T0: network launches, T1: SafeTrade listing, T2: Xeggex/NonKYC, T3: MEXC/Gate, T4: mainstream.
Discovery score = how early venue lists legitimate network vs market.

### Exchange funnel
GitHub/mainnet → NonKYC/XeggeX/SafeTrade → MEXC → Gate/KuCoin → major venues.

### Live venues
- SafeTrade (10bps maker/taker, flat)
- NonKYC (obscure PoW/privacy, BTC Blake2B listed Sep 5 2026)
- XeggeX ($5 listing fee, $400 min liquidity)
- MEXC Assessment Zone
- TradeOgre = historical training set only

### Frontier Compute Index (FCI)
FCI-PQ, FCI-POW, FCO-PRIV, FCI-COMP, FCI-ZK, FCI-SAFE subindices.

### Four entries per listing
A. announcement price, B. +24h, C. +7d, D. first 30% drawdown.

### Ledger fields
project_id, ticker, network, launch/listing dates, prices at intervals, mcap/fdv/volume at listing, technical flags, premine/distribution, GitHub metrics, later exchanges, return_usd, return_btc, max_drawdown/gain, alive status.

### Key QUBIC thesis
$58-60m mcap, burn mechanism (41.5T burned by May 2026), halving Aug 19 2026, computational economy with direct token sink. Ventrue-stage crypto trading publicly.

### Key QUAN thesis
ML-DSA PQ + Poseidon2 PoW + ZK privacy + 21m cap. 27% genesis (23% investors/founders/team), 73% mineable. Venture-stage crypto publicly.

### TradeOgre
Historical training set. NonKYC became remaining CEX after mid-2025 demise.

## Execution: feed not spreadsheet
SafeTrade + NonKYC + Xeggex listing event → classify → freeze fundamentals → collect candles/orderbook → continuously report cohort performance.
