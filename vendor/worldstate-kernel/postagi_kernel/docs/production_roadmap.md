# Production roadmap

## Phase A — point-in-time evidence lake

Ingest and retain raw + normalized records from SEC EDGAR, arXiv/OpenAlex, PatentsView, clinical trials/regulators, government procurement, trade/supply-chain data, company filings/transcripts, GitHub/model benchmarks, capex/lead-time disclosures, and market/fundamental data. Preserve publication timestamp, retrieval timestamp, source identity and content hash.

## Phase B — technology graph

Run the TechToken-compatible IPC-context pipeline and semantic-triple convergence pipeline on rolling windows. Materialize `technology -> technology`, `paper -> technology`, `patent -> technology`, and `company -> patent/technology` edges. Keep raw term aliases plus stapled topic IDs so clustering decisions are auditable.

## Phase C — future-state ensemble

Represent 1y/2y/5y states as a set of partially dependent scenario primitives rather than one AGI date. Use calibrated forecasters/LLMs to propose likelihood ratios but require source citations and store pre/post probabilities. Score calibration using Brier/log loss against resolvable intermediate events.

## Phase D — economic propagation

Build signed causal paths from capabilities to cost curves, substitution, demand, profit pools and securities. Estimate elasticities from historical analogues where possible; otherwise encode distributions, not point estimates. The valuable query becomes: **which present cash flows are inconsistent with most high-probability future worlds?**

## Phase E — market-implied probability

Fit scenario exposures jointly to valuation residuals, earnings revisions, options/skew where available, event-window returns and cross-sectional prices. Refuse precise output when the exposure matrix is ill-conditioned.

## Phase F — live paper portfolio

Daily/weekly rebalance only after point-in-time validation. Log every signal decomposition, causal path, evidence update and market-implied gap. Start with a paper portfolio and compare to simple factor/sector baselines before deploying capital.
