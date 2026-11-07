# WORLDCAST

**Forecast the world. Understand its dynamics. Control its future.**

WORLDCAST is an experimental research environment for studying the path from multivariate time-series forecasting to predictive world models and decision-making. The v0.1 prototype includes a deterministic synthetic transport-world simulator, intervention hooks, forecasting baselines, a reproducible benchmark and a browser-based control-room demo.

> Research prototype: this is not an OpenTTD fork. The simulator is standalone so its data contract and experiments can be validated before game-engine integration.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m worldcast.cli simulate --steps 1000 --cities 20 --seed 7 --out data/world.csv
python -m worldcast.cli benchmark --steps 1000 --cities 20 --seed 7
python -m pytest
```

Open `web/index.html` in a modern browser for the interactive demo. No server or external API is required.

## Research questions

1. Can a forecasting model generalize to held-out cities and unseen world seeds?
2. Does multivariate context improve forecasts over per-city univariate baselines?
3. Can models predict interventions such as capacity expansion, station closure and demand shocks?
4. Do better forecasts produce better decisions, measured by cumulative utility and regret?

## Environment

Each synthetic city has population and economic activity, passenger and cargo demand, rail capacity, congestion, revenue and weather. Cities are coupled through a demand network; exogenous shocks and interventions perturb the system. Values are synthetic units, not real-world transport measurements.

## Baselines

- Persistence
- 52-step seasonal naive
- Ridge autoregression with local lags and network context

Metrics: MAE and RMSE. These are reference baselines, not claims about foundation-model performance. Planned adapters include TimesFM, Chronos and Moirai with pinned versions and identical rolling-origin splits.

## Roadmap

- [x] Deterministic coupled-city simulator and reproducible data export
- [x] Intervention hooks and forecasting baselines
- [x] Interactive browser prototype
- [ ] OpenTTD adapter and scenario extraction
- [ ] TimesFM / Chronos / Moirai adapters
- [ ] Probabilistic calibration (CRPS, coverage)
- [ ] Counterfactual transition-model evaluation
- [ ] Model-based planning and decision regret
- [ ] Held-out topology and distribution-shift benchmark suite

## License and attribution

Original WORLDCAST prototype code is MIT licensed. OpenTTD is a separate project with its own license and assets; this repository does not bundle OpenTTD code or game assets. Any future fork or redistribution must comply with upstream license and asset terms. See `THIRD_PARTY_NOTICES.md`.

Built with curiosity by Dipayan.
