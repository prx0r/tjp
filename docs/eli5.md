# ELI5 — why a trade is doing well (2026-09-12, saved word for word)

## The abstraction

> **A sector explodes when a fast-growing, extremely valuable end-market collides with a slow,
> indispensable input whose buyers can absorb much higher prices without changing behavior.**

That is the whole memory trade.

## The formula

$$
BRP =
\frac{
V \times I \times W \times L \times Q
}{
E \times S
}
$$

- **V = downstream value growth** — how valuable is the thing being built?
- **I = indispensability** — can production happen without this input?
- **W = willingness to pay** — does doubling this input's price materially alter customer economics?
- **L = lead time** — how long until new supply appears?
- **Q = shortage intensity** — backlog, utilization, inventory depletion, spot premiums
- **E = supply elasticity** — how quickly can capacity expand?
- **S = substitution ease** — can buyers switch to something else?

$$
TradeScore = BRP \times ValuationGap \times Reflexivity \times Catalyst
$$

Great industry ≠ great trade. Monitor six series per sector:
**end demand → utilization → inventory/backlog → lead time → price → new capacity**.
Alert when demand ↑ + utilization → 100% + inventory ↓ + lead time ↑ + price ↑ while 2-year
capacity stays insufficient = "a bottleneck has become a trade."

## Ten bottleneck trades 2024–2026 (five-sentence form each)

1. **Memory / HBM — canonical.** AI compute value ↑↑ (Reuters: ~$800B 2026 data-center spend vs ~$200B 2024);
   every accelerator needs fast memory, HBM eats fab capacity; supply sold out, ≥2y new fabs;
   hyperscalers accept huge premiums (open-ended Micron asks); SK Hynix +~340% in a year, ~57% HBM. ([Reuters][1])
2. **Transformers / switchgear.** Tens of GW new electrical need; data center can't run without them;
   lead times >160 weeks, utilities ordering 5y ahead; tiny vs $5–20B campus value → scarcity rent to slots. ([Reuters][2])
3. **Gas turbines.** AI needs power now; 24/7 firm power = gas; slow manufacturing; dead data center
   costs more than any turbine premium; GE Vernova doubled 2024 orders, ≥110 GW backlog/slots, $200B by 2027. ([Reuters][3])
4. **European defense.** Invasion made it necessity; ammo/air-defense capacity can't respond;
   multi-year factories/labor/qualification; governments aren't price-sensitive; aero/defense index +~55% to Jan 2026. ([Reuters][4])
5. **Uranium.** AI revived power growth; plants need fuel regardless; mines/fuel-cycle ultra-slow, US output
   far below use; utility pays rather than shuttering multi-B$ plants; miners +100%+. ([Reuters][5])
6. **Copper.** AI+grid+EV conductor demand; hard to substitute; mines take years, quality falling;
   modest share of project value → tolerance; +40–42% in 2025, records above $13–14k/t. ([Reuters][6])
7. **Oil tankers.** Cargo must move; chokepoints raise ship-miles, remove vessels; can't print VLCCs;
   $10–100m cargoes move anyway; Gulf-China ~$11.50/bbl records. NOT permanent — vanishes on normalization (Maersk warned). ([Reuters][7])([Reuters][8])
8. **Gold miners.** Fiscal/geopolitical + central-bank demand; mines can't respond fast; years to build;
   above fixed cost, price drops to margin; gold +64% in 2025 (best since 1979). ([Reuters][9])
9. **Semi equipment / EUV.** AI silicon ultra-valuable; no advanced chips without it; near-monopoly tools;
   $200M tool unlocks B$s of wafers; EUV booked through 2027, ASML +30% capacity, guidance raised. ([Reuters][10])
10. **Power architecture / microgrids.** Demand outruns grid connections; unpowered campus ≈ worthless;
    queues/equipment slow; time-to-power > ¢/kWh; Vertiv's $1.45B+ deal for Utility Innovation Group. ([Reuters][11])

## The universal five

> 1. Something downstream became much more valuable.
> 2. It cannot scale without X.
> 3. X cannot increase supply quickly enough.
> 4. X is cheap relative to the value it unlocks, so buyers tolerate huge price increases.
> 5. Therefore X captures scarcity rent until capacity, substitution or downstream demand catches up.

$$
\boxed{ ScarcityRent \approx \frac{\text{Value unlocked by one more unit}}{\text{Cost of that unit}} \times \frac{\text{Time to add supply}}{\text{Ease of substitution}} }
$$

## Machine form

100–200 sector/input nodes, fields: end_value_growth, capacity_utilization, inventory, lead_time,
backlog, spot_price, contract_price, capacity_additions, substitution, buyer_margin, buyer_capex.
Boring primary feeds (TrendForce, Baltic/Freightos, LME/CME, EIA/IEA, FERC queues, NATO/EDA, bookings, Reuters).
Output shape: `HBM MEMORY — 94/100 … State: SCARCITY RENT ACTIVE. Kill: inventory rebuild + lead times fall + capacity overtakes demand.`

[1]: https://www.reuters.com/world/china/ai-frenzy-is-driving-new-global-supply-chain-crisis-2025-12-03/
[2]: https://www.reuters.com/business/energy/us-power-companies-scramble-secure-equipment-surging-data-center-demand-strains-2026-07-09/
[3]: https://www.reuters.com/business/energy/ge-vernova-posts-rise-quarterly-profit-misses-revenue-estimates-2025-01-22/
[4]: https://www.reuters.com/business/aerospace-defense/how-war-has-reshaped-europes-defence-sector-2026-01-14/
[5]: https://www.reuters.com/markets/commodities/is-us-uranium-market-about-go-nuclear-2026-2026-01-14/
[6]: https://www.reuters.com/world/americas/record-copper-price-signals-accelerating-race-supplies-2026-01-05/
[7]: https://www.reuters.com/business/energy/oil-tanker-rates-hit-record-highs-following-iran-us-shipping-attacks-2026-09-11/
[8]: https://www.reuters.com/business/maersk-q4-meets-forecasts-falling-freight-rates-weigh-2026-profits-2026-02-05/
[9]: https://www.reuters.com/world/africa/gold-miner-shares-jump-bullion-prices-hit-5100oz-record-high-2026-01-26/
[10]: https://www.reuters.com/business/asml-tops-q2-estimates-ai-chip-demand-2026-07-15/
[11]: https://www.reuters.com/legal/transactional/vertiv-strikes-145-billion-deal-microgrid-firm-utility-innovation-group-2026-09-02/
