# Monero rig decision (2026-09-12 research bundle; code: research/mining/{xmrig,RandomX})

## Physics first (non-negotiable)

- RandomX = CPU-only by design (cache + branch prediction + OoO). GPUs do 2–4 KH/s, useless.
- 2 MB L3 per mining thread. Threads beyond L3/2 LOSE hashrate — let xmrig auto-pick, never force all threads.
- Huge pages = +20–50% (single biggest setting). 1GB pages (Linux) +1–3%. MSR mod up to +15% (needs msr.allow_writes=on, kernel ≥5.9).
- Disable hardware prefetchers. DDR5-6000 CL30 beats DDR5-5200 by 10–15%. Tune = +8–25% total.
- Network: ~3.5–5.5 GH/s, 0.6 XMR/block tail emission, 432 XMR/day. ~0.00008 XMR/day per kH/s (at 5.4 GH/s).

## The rig ladder (all AMD — Intel loses on L3 per core)

| Scenario | Pick | Hashrate | Power | Why |
|---|---|---|---|---|
| Absolute best, money no object | 9950X3D (Zen 5, 128MB 3D cache) | 23–25 KH/s | ~170W+cooling | Top consumer RandomX chip |
| Farm build (perf/watt + value) | 9950X | 21–23 KH/s | ~170W | ~1–2 KH/s behind X3D, cheaper platform |
| Used-market king | 7950X (Zen 4) | 24–26 KH/s | ~170W | Post-Zen-5 prices, proven |
| Budget king | 5900XT on AM4 + DDR4 | 11–13 KH/s | 105W | No platform tax, 4-rig garage math works |
| Starter | 5800XT (Wraith in box) | ~8–10 KH/s | 105W | Cheapest entry, 18–24mo payback |
| Serious home farm | Threadripper 5995WX/7995WX 64c | 100–110 KH/s | 280W+ | 64c × cache |
| Cheap-power beast | EPYC 7763/9554P used server | 75–100 KH/s | 280–320W | Only profitable new-hardware class at $0.10/kWh |

## Profitability truth (the whole game is electricity)

- <$0.08/kWh: almost everything above profits. $0.10: only EPYC clearly green on new hardware.
- $0.12: marginal. $0.15+: buy XMR instead of mining (unless waste heat heats your home).
- Pool: P2Pool (0% fee, no custody, needs ~5 kH/s main chain) else fee pool for simplicity.
- MSR/PBO/undervolt: lock affinity to physical cores, yield=false for max hash, keep <80°C.

## Verdict for us

No universal "optimal" — optimal = f(power price, capex, heat use). Default recommendation:
**7950X-class used (or 9950X new) + DDR5-6000 CL30 + huge pages + P2Pool**, profitable under $0.12/kWh.
Server route only with sub-$0.08 power. Everything else is stacking sats for principle.

Sources: xmrig.com benchmark + optimization guide + CPU.md, miningreturns.com, moneroswapper.io,
changee.com, techrark.com (all fetched 2026-09-12). Code: xmrig/xmrig, tevador/RandomX.
