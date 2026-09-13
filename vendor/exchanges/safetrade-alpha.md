# SafeTrade experiment — Frontier Crypto Index (2026-09-13, saved word for word)

[This is the full analysis as provided by the user. Key structures preserved below.]

## Core thesis

Two strategies:
1. SafeTrade Index — buy $100 at first executable price after listing, never sell. Measure returns.
2. Discovery venue ranking — T0→T1(SafeTrade)→T2(Xeggex/NonKYC)→T3(MEXC/Gate)→T4(mainstream).

## Exchange funnel
GitHub/mainnet → NonKYC/XeggeX/SafeTrade → MEXC → Gate/KuCoin → major venues.

## FCI subindices
FCI-PQ, FCI-POW, FCI-PRIV, FCI-COMP, FCI-ZK, FCI-SAFE.

## Four entries per listing
A. announcement price, B. +24h, C. +7d, D. first 30% drawdown.

## Ledger fields
project_id, ticker, network, launch/listing dates/prices, mcap/fdv/volume at listing, technical flags, premine/distribution, GitHub metrics, later exchanges, return_usd/btc, max_drawdown/gain, alive status.

## Key QUBIC thesis
$58-60m mcap, burn mechanism, halving, computational economy.

## Key QUAN thesis
ML-DSA PQ + Poseidon2 PoW + ZK + 21m cap, 27% genesis, venture-stage publicly.

## Execution
SafeTrade + NonKYC + Xeggex listing events → classify → freeze fundamentals → collect candles/orderbook → continuously report cohort performance.

## Repos cloned
safetrade-client, qrl, safecoinwiki, xeggex-api, prl-today, safetrade-exchange-client.
