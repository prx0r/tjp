# Post-AGI World-State / Obsolescence Kernel — Build Report

Build date: 2026-09-10

## Verification

- Unit tests: **12 passed**.
- End-to-end demo: **passes** from a raw source checkout and writes ranking/backtest artifacts under `reports/`.
- Composite score sign check: positive Song Ma technological obsolescence is treated as an **incumbent penalty**, not a beneficiary signal.
- Backtest harness uses point-in-time score semantics, forward returns, turnover, and explicit transaction costs.

## Research kernels implemented

1. **TechToken / Fenoaltea et al. (arXiv:2605.04875)** — exact published top-1% pairwise cosine aggregation over context-specific technology embeddings; embedding-model training remains an external adapter.
2. **Technological Obsolescence / Song Ma** — fixed external technology base and exact `-[ln(Cit_t)-ln(Cit_t-w)]` transformation.
3. **Semantic technological convergence / Sternfeld et al. (arXiv:2510.25370)** — q-gram similarity, soft-cardinality Dice noun stapling, 0.85 stapling threshold, Louvain resolution 0.85, eigenvector centrality, temporal Jaccard.
4. **Predictive Patentomics / Yang (arXiv:2307.01202)** — text-embedding plus patent-structure feature path, temporal split, acceptance/value neural-network heads. Historical OpenAI `ada-002` embeddings are not misrepresented as reproduced.
5. **MIRAI / Ye et al. (arXiv:2407.01231)** — temporal structured-event retrieval/forecast contract plus deterministic offline baseline; authors' full ReAct implementation is pinned externally.
6. **Supply-chain production functions / Chang et al. (arXiv:2407.18772)** — production-attention/inventory primitives and a bottleneck extension; full SC-TGN/SC-GraphMixer repository is pinned externally.
7. **Agentic Trading (arXiv:2605.19337)** — its reproducibility warnings are turned into explicit backtest constraints instead of copied as a trading signal.
8. **Lopez-Lira & Tang (arXiv:2304.07619)** — used as an architectural constraint: first-order LLM-readable textual alpha should be assumed to decay, pushing the engine toward multi-hop causal propagation.

## Kernel architecture

`evidence -> scenario probability updates -> future-world distribution -> typed causal graph -> company cash-flow exposure -> market-implied scenario inversion -> divergence -> cross-sectional ranking -> walk-forward backtest`

The causal graph uses signed edges with elasticity, confidence and delay. The inverse-pricing module solves a bounded ridge least-squares problem for market-implied scenario probabilities and exposes matrix conditioning so the system can refuse false precision.

## Demo company screen

The bundled 36-company universe is an **illustrative integration fixture**, not a claim based on live measured patent/fundamental data. After the corrected obsolescence sign, the highest fixture scores are NVIDIA, Recursion Pharmaceuticals, ASML, TSMC and CRISPR Therapeutics. The most negative fixture scores are EPAM, Globant, Accenture, Salesforce and Intuit.

These outputs demonstrate that the causal signs propagate coherently: the seeded post-AGI world raises scarce compute/semiconductor/life-science-tool exposure and penalizes long-duration labor/software-rent cash flows. They must not be interpreted as validated investment recommendations.

## Synthetic backtest smoke test

The deterministic synthetic 2019–2025 monthly panel reports:

- Annualized return: **8.77%**
- Annualized volatility: **6.42%**
- Sharpe: **1.37**
- Maximum drawdown: **-8.37%**
- Transaction cost assumption: **10 bps of turnover**
- Rebalance periods: **84**

This is deliberately a **software/logic validation fixture with planted signal**, not empirical evidence that the strategy earns those returns.

## External repositories pinned

The ZIP records exact commit SHAs for MIRAI, the Stanford supply-chain implementation, Song Ma's patent-firm linkage data, `backtesting.py`, and Microsoft Qlib in `external/manifest.json`. `scripts/bootstrap_external.sh` clones those exact revisions on an internet-connected machine.

The execution sandbox used for this build could inspect GitHub through the authenticated connector but did not have direct Git DNS access, so third-party repositories are **not vendored into the archive**. This also avoids silently redistributing repositories with differing licenses.

## Production work needed before capital deployment

Replace demo exposures and auxiliary scores with timestamped point-in-time data: patent citations/IPC context, arXiv/OpenAlex research graph, SEC filings and estimates, options/valuation residuals, supply-chain/lead-time data, clinical/regulatory events, procurement/capex, and survivorship-safe market history. Calibrate 1y/2y/5y scenario probabilities against resolvable intermediate events using Brier/log loss, then run sector/factor-neutral walk-forward tests with realistic borrow/slippage/capacity assumptions.
