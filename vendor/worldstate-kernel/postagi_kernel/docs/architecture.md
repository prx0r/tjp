# Architecture

## Core object

The investable quantity is not `future - present`. It is:

`(our probability of future state - market-implied probability) × cash-flow exposure × duration × confidence`.

The architecture deliberately separates the four inference problems:

1. **World model** — what states are plausible at 1/2/5+ years?
2. **Evidence update** — what new paper, patent, benchmark, filing, shipment, lead-time, trial, capex or policy fact changes a state's probability?
3. **Causal propagation** — if state S occurs, which capabilities/costs/behaviors/demand pools/company cash flows change?
4. **Reverse pricing** — what state probabilities are already implied by current cross-sectional prices/valuation residuals?

## Typed graph

`WorldGraph` supports the causal chain:

```
world_state
  -> capability
  -> cost_curve / constraint
  -> behavior
  -> demand
  -> profit_pool
  -> company
```

Every edge has a signed elasticity, confidence and causal delay. The static kernel enforces a DAG; feedback loops should be modeled by a dynamic state-space extension rather than accidentally recursive edges.

## Evidence graph

Evidence records are atomic and timestamped:

```
{id, timestamp, source_type, target_scenario,
 log_likelihood_ratio, reliability, description}
```

`scenario.py` updates prior odds by log-likelihood ratios. Reliability tempers evidence when source-dependence is not yet explicitly modeled. A production version should add source-family correlation clusters so ten articles repeating one primary result do not count as ten independent observations.

## Technology leading indicators

Three independent early-warning channels are intentionally kept separate:

- **TechToken:** linguistic convergence between IPC technologies before first combination.
- **Semantic triple graph:** convergence of research/patent topics through increasing co-publication Jaccard.
- **Ma obsolescence:** decay in external use of the *existing* fixed technology base.

This separation is useful: the first two detect what is forming; the third detects what is dying.

## Company scoring

Positive score means the configured future-world divergence is favorable to cash flows. Negative means cash flows appear structurally at risk. In deployment, the score should be decomposed into scenario contributions and causal paths; never trade a scalar without inspecting its evidence and path provenance.

## Reverse market model

`market_implied.py` solves a bounded ridge inverse problem:

`priced_impacts ≈ company_scenario_exposure_matrix × market_probabilities`.

This is intentionally diagnostic, not magical identification. Highly correlated scenario exposures create a poorly conditioned inverse problem; `condition_number()` is exposed so the engine can refuse false precision.
