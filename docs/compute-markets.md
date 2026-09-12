# Cheap compute for XMR (2026-09-12 bundle)

Goal: run xmrig where CPU is cheapest. Honest baseline: rented CPU is usually priced ABOVE its
mining yield (else providers would mine). Profit paths: free trial credits, mispriced listings,
waste/idle capacity you already control. Everything below is setup-ready; economics per rig in
`docs/mining-rig.md`.

## Akash (best fit: any Docker image, CPU-first)

- Console (managed, card billing, trial credits) or CLI/SDL self-custody (Keplr, AKT→ACT escrow).
- Trial limits: short-lived deployments (~24h auto-close), no high-end GPUs — CPUs fine.
- Flow: SDL (below) → create deployment → accept bid → send manifest → per-block escrow billing.
- xmrig SDL: `research/compute/xmrig-akash-sdl.yaml` (tune cpu units to L3/2 threads, pool + wallet via env).
- Watch: escrow drain = auto-close; set spend caps; trial is for measurement, not income.

## Golem (best fit: burst sweeps across many providers)

- JS Task API (`@golem-sdk/golem-js`), `try_golem` test key on hoodi testnet, GLM on mainnet/polygon.
- Demand: workload image + minCpuThreads + linear price caps (start/env/cpu per hour).
- Model is task rentals (rentHours), not 24/7 servers — good for benchmark sweeps and short mining bursts,
  awkward for always-on rigs. Filter providers by price (example custom filter in docs).
- xmrig task example: `research/compute/golem-xmrig-task.mjs` (adapt image + wallet + pool).

## Others (ranked for RandomX)

- **MiningRigRentals / NiceHash**: rent RandomX hashpower directly — price discovery for what hashes cost;
  buy only below your measured yield. Best for spike capacity, not base load.
- **Vast.ai**: GPU-first marketplace, per-second billing, interruptible deals. CPU instances exist but
  RandomX wants cache-rich AMD — verify L3/thread before bidding; usually GPU-priced, usually a loss.
- **Flux**: decentralized CPU+GPU cloud, Docker-based like Akash. Worth a quote comparison.
- **Salad**: gamer-PC pool, GPU-oriented. Skip for RandomX.

## Verdict ladder

1. Free credits (Akash trial) → free hashes, measure real yield first.
2. Existing idle hardware (home/server) → still king under $0.12/kWh.
3. Mispriced spot CPU (any marketplace) → arbitrage while it lasts, auto-exit on price.
4. Sustained rented CPU at list price → almost always negative. Don't.

Sources: akash.network/docs, docs.golem.network (fetched 2026-09-12).
