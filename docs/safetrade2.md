# SafeTrade data stack — four alpha datasets (2026-09-12, saved word for word)

CoinGecko is banned from this pipeline. Replacement: SafeTrade's own ticker/markets, Zendesk
announcement archive, hashrate.no coin/GPU pages, pool telemetry (AlphaPool, LuckyPool, prlscan).

## 0. Sources

- SafeTrade org `safetrade-exchange`: example client (account/order methods + `global.tickers`
  WebSocket stream) ([GitHub][1])([GitHub][5]). Public Markets page scrapeable: market, price, 24h
  high/low, amount, volume; currently PRL, QUBIC, QTC, QUAN, TSC, XEL, XTM, WART, NOID ([SafeTrade][2]).
- Zendesk archive = historical listing database incl. old listings/migrations (BTCZ, RVN, CLORE, QUBIC,
  ZEPH/XMR) ([Help][3]). Precise timestamps: TSC Aug 17 22:02, QUAN Sep 9 22:06, Parano1d Sep 1 11:49 ([Help][4]).
- `stlin256/prl-today`: Pearl revenue monitor on SafeTrade ticker + PRLScan + pool stats ([GitHub][10]).

## 1. safetrade_listing_history

symbol, project, announcement_time, first_market_seen_time, first_trade_time, pair, first_bid,
first_ask, spread, depth_1pct, depth_5pct, 24h_volume_at_T0, exchange_number, coin_age_days,
github_created_at, mainnet_age_days, market_cap_estimate, sector, mineable, algorithm.
Snapshot SafeTrade every 1–5 min. Key trick: detect new markets BEFORE announcement
(market/API → wallet → deposit → orderbook → announcement). Diff /markets, fees, deposit list,
API metadata, WS ticker keys, support sitemap, org activity.

## 2. Mining dataset (better)

coin, ts, price, hashrate, difficulty, reward, block_time, emission, miners, workers, pools,
largest_pool_share, GPU_model/hashrate/power, revenue_per_GPU, profit_per_GPU, revenue_per_watt,
miner_release_count, new_pool_count, SafeTrade_volume.
Mining Mispricing Ratio = daily mineable value / network compute cost.
Infrastructure Growth (Δpools/miners/workers/hashrate/repos/benchmarks) vs Δprice/Δvolume.
Signal: infra exploding while price/attention flat.

## 3. hashrate.no inputs

Price, revenue+ precipitationyield per unit hashrate, network hashrate, difficulty, reward, block time,
GPU benchmarks, pools. QUAN: ~15–22 TH/s, ~0.30 reward, $/day per GH/s ([Hashrate][6]).
RTX 5060 on QUAN: ~232 MH/s @96W ≈ $1.19/day rev, ~$0.95 profit ([Hashrate][7]).
Compute $/GPU-day, $/kWh, $/VRAM, $/purchase, $/rented-hour vs cloud markets.

## 4. Pool telemetry

AlphaPool Pearl: per-GPU rates, share, miners, workers, blocks, payments (H100 ~700 TH/s,
5090 ~372, 4090 ~311, 3090 ~110) ([AlphaPool][8]). prlscan calculator on live difficulty +
SafeTrade price ([prlscan][9]). Deterministic stream: SafeTrade price + emission + hashrate +
benchmarks + fee + power cost = realtime profitability. No LLM.

## Ticker-collision warning

Minerstat maps PRL to Binance/Coinbase futures — WRONG Pearl ([Minerstat][11]). NEVER join on symbol.
Canonical identity: chain_id, genesis_hash, github_repo, official_domain, contract, explorer.

## Who's interesting now

QUAN first (young, Sep 9, benchmarks+pools, fast-moving) ([Help][12]). Pearl next (mature infra,
~24 EH/s snapshot, full GPU economics) ([Hashrate][13]). TensorCash stranger (Proof-of-Inference,
~40 KPoI/s, 111 miners/563 workers, 55.6 TSC reward, 3% fee) ([LuckyPool][14]). XEL benchmarks
(~16 MH/s) ([Hashrate][15]). XTM RandomX revenue/KH/s, ~95 MH/s ([Hashrate][16]). WART accessible
([Hashrate][17]). Qubic: hashrate.no stale — source from ecosystem ([Hashrate][18]).

## Alpha engine (not "most profitable today")

NEW/OBSCURE PoW → SafeTrade universe → chain metrics → pools → benchmarks → cloud/power costs →
market/liquidity → MINING_EDGE (revenue_per_compute × liquidity × youth × infra_growth × emission ÷
competition) + DISCOVERY_EDGE (quality × infra_growth × earlyness × GitHub × demand_growth ÷ valuation).
Sweetest: listed + 3 new pools + accelerating miner releases + 15%/day hashrate + rentable profit + flat price.
One layer earlier: new coins on hashrate.no, new pool subdomains, new miner releases, GitHub integrations.

[1]: https://github.com/safetrade-exchange/example-client/blob/master/api.py
[2]: https://safetrade.com/markets
[3]: https://support.safetrade.com/hc/en-us/sections/360002787112-Announcements?page=3
[4]: https://support.safetrade.com/hc/en-us/articles/48211939667725-TensorCash-TSC-has-been-listed-on-SafeTrade
[5]: https://github.com/safetrade-exchange/example-client/blob/master/manager.py
[6]: https://www.hashrate.no/coins/quan
[7]: https://www.hashrate.no/gpus/5060/QUAN
[8]: https://pearl.alphapool.tech/miners/
[9]: https://prx0r.com/tools
[10]: https://github.com/stlin256/prl-today
[11]: https://minerstat.com/coin/prl
[12]: https://support.safetrade.com/hc/en-us/articles/48787585602317-Quantus-QUAN-has-been-listed-on-SafeTrade
[13]: https://hashrate.no/coins/PRL/calculator
[14]: https://tensorcash.luckypool.io/
[15]: https://hashrate.no/coins/XEL/
[16]: https://www.hashrate.no/coins/XTM-RX/calculator
[17]: https://hashrate.no/coins/WART/calculator
[18]: https://hashrate.no/coins/QUBIC/calculator
