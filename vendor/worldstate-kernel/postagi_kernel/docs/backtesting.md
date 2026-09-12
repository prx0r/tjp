# Backtesting protocol

The built-in backtester is deliberately small because the principal failure mode is not missing execution features; it is **look-ahead leakage**.

Required production rules:

- Every evidence item, filing, patent publication, price, fundamental, scenario probability and company-universe membership carries an `asof` timestamp.
- Signal at date `t` can only consume records available at or before `t`.
- Return label is explicitly `t -> t+1`; never merge a same-period realized return into feature construction.
- Survivorship-free universes are required for historical claims.
- Delisted securities remain in the historical universe and delisting returns must be handled where the data source provides them.
- Transaction costs are charged on turnover. Add spread/slippage/borrow separately for a realistic short book.
- Hyperparameters are trained on the past only. No random cross-validation across time.
- Compare against sector-neutral, beta-neutral and ordinary factor baselines before calling world-state signal "alpha".
- Store the exact scenario-prior snapshot and graph hash used for each historical signal.

The included `demo_backtest_panel.csv` is **synthetic** and exists only to verify that the software recovers a planted cross-sectional signal without leakage. Its Sharpe ratio is not empirical evidence that the strategy works.

For real replication, use CRSP/Compustat or an equivalently point-in-time dataset, the Song Ma public patent-firm panel where applicable, and a licensed historical fundamentals/price feed. `external/manifest.json` pins backtesting.py and Qlib for independent execution-engine cross-checks.
