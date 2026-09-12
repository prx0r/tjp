# Post‑AGI World‑State / Obsolescence Kernel

A research kernel for the thesis:

> **Find future worlds whose probabilities are mispriced, then find today's cash flows that cannot coexist with those worlds.**

Instead of predicting a stock price directly, the kernel decomposes the problem into world-state probabilities, causal cash-flow exposure, technological obsolescence/convergence, market-implied probabilities, and a point-in-time backtest.

## What is working

- TechToken paper's top-1%-pair context-similarity aggregation for contextual IPC embeddings.
- Song Ma technological-obsolescence formula from a fixed external technology base.
- Sternfeld et al. noun stapling + 0.85 threshold + Louvain/Jaccard convergence primitives.
- Predictive-Patentomics-compatible embedding + structural supervised models with temporal split.
- MIRAI-style temporal event-forecast interface.
- Supply-chain inventory/production-function abstraction + physical bottleneck extension.
- Typed signed causal graph: world state -> capability -> cost -> behavior -> demand -> profit pool -> company.
- Bayesian log-odds evidence updates.
- Reverse market-probability inference with bounded ridge least squares and conditioning diagnostics.
- Long/short walk-forward backtest with turnover and transaction costs.
- 36-company post-AGI demo universe and explicit scenario priors.
- SQLite evidence/snapshot store and production adapter contracts.
- 12 unit tests.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pytest -q
postagi-demo
```

The demo writes rankings and backtest diagnostics to `reports/`.

## Critical interpretation warning

`data/demo_companies.csv` contains **illustrative manually seeded causal exposures**, not measured live exposures or investment recommendations. `data/demo_aux_scores.csv` is also a fixture. `data/demo_backtest_panel.csv` is deterministic synthetic data for testing the engine, not historical market evidence.

A production claim requires point-in-time prices/fundamentals, survivorship-safe company membership, real patent/research/supply-chain signals, and calibrated scenario probabilities. See `docs/backtesting.md` and `docs/production_roadmap.md`.

## Paper-scale reproduction boundaries

Some papers require large proprietary/public corpora and substantial GPU compute. This ZIP implements exact published formulas/aggregations where they can be reproduced locally and pins original repositories for full reference implementations. It does **not** pretend that a hash embedding or toy dataset is the trained TechToken model, that a deterministic temporal baseline is MIRAI's LLM agent, or that the lightweight inventory module is the authors' SC-TGN.

Use `./scripts/bootstrap_external.sh` on an internet-connected machine to clone the inspected repositories at the exact commits recorded in `external/manifest.json`.

## Layout

```
postagi_kernel/
  methods/             # paper-derived kernels
  world_graph.py       # typed causal propagation
  scenario.py          # evidence -> probabilities
  market_implied.py    # reverse-price state probabilities
  scoring.py           # security-level world divergence
  backtest.py          # point-in-time cross-sectional test
  adapters.py          # live data contracts
  store.py             # evidence snapshots
configs/                # world-state priors
external/               # pinned original repos / bootstrap
scripts/                # demos and bootstrap
data/                   # clearly marked fixtures
reports/                # generated outputs
docs/                   # methods, architecture, protocol, roadmap
tests/                  # unit tests
```

## Formula

For scenario `s` and company `i`, the base security signal is approximately:

```
Σ_s [(P_ours(s)-P_market(s)) × exposure(i,s) × horizon_weight(s)]
× duration(i) × evidence_confidence(i)
```

The composite then treats positive technological obsolescence as an incumbent penalty and adds independent convergence/patent-quality channels.
