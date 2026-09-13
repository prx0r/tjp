# Death Token Strategy v2 — Mirror image of SafeTrade long study

Saved from message 2026-09-13. Core insight: "these things statistically decay" is an excellent signal even when short isn't directly executable.

## Death Pressure Ratio (DPR)

D = (E_m + E_u + E_i) / (V_o × L_q)
DPR = daily newly liquid supply USD / daily genuine spot volume USD

## Additional metrics
- FDV / float market cap
- emission / circulating supply
- miner profitability
- volume decay after listing
- buyer concentration
- spread/depth
- number of independent venues
- organic usage / token sink

## Strategies
- DEATH-0: short every new listing
- DEATH-1: short after initial pump (+24h)
- DEATH-7: short at +7 days
- DEATH-FADE: wait for volume peak + 50% decline
- DEATH-SUPPLY: short when DPR > threshold
- DEATH-FDV: short when FDV/float > threshold
- DEATH-MINER: short when daily emission/spot > threshold
- DEATH-COMBINED: high supply pressure + low demand + low liquidity + no token sink

## Execution classification
- THEORETICAL_SHORT: price eventually collapsed
- SHORTABLE_DEATH: borrow/perp available
- EXECUTABLE_DEATH: depth allowed our size
- SURVIVABLE_DEATH: MAE stayed below risk threshold

## Long-short frontier
Top quintile FRONTIER LONG (Qubic-like, actual utility, token capture)
Bottom quintile DEATH SHORT (FDV/float distortion, no users, no token sink)
R_LS = R_Frontier - R_Death

## Quantus as case study (frozen Sep 13, 2026)
Bull: genuine tech innovation, PQ narrative, working mainnet, real miners, 21m cap, early discovery
Bear: ~$1B implied FDV, tiny float, expanding miner supply, no demonstrated monetary demand, thin liquidity
Forecast: absent major catalyst, newly emitted supply should cause QUAN to underperform BTC over 30/90/180 days.
Labels: Y_30, Y_90, Y_180 = R_QUAN - R_BTC
