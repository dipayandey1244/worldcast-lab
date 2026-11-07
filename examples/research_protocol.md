# WORLDCAST v0.1 research protocol

## Core hypothesis
A model that learns useful representations of a coupled dynamic world should support both accurate forecasts and better decisions under interventions. Forecast accuracy alone is insufficient evidence of world understanding.

## Experimental protocol
1. Fix simulator version, seed list, city count and network coupling.
2. Split chronologically; never randomly mix future observations into training.
3. Report metrics per city and horizon, plus aggregate metrics.
4. Compare local-only, multivariate-context and intervention-aware models.
5. Evaluate held-out seeds, held-out cities, missing observations and shocks.
6. For action evaluation, compare policies on identical initial states and random seeds.
7. Report uncertainty intervals and all failed runs.

## Metrics
- Forecasting: MAE, RMSE, CRPS, interval coverage and calibration.
- Dynamics: transition prediction error and state consistency.
- Decisions: cumulative utility, regret, congestion and service level.
- Robustness: degradation under shocks, missingness and topology shift.

## Baselines
Persistence, seasonal naive and ridge context are initial reference points. Add pretrained TSFMs only with documented model versions, preprocessing, context lengths and compute budgets.

## Caution
Synthetic performance does not establish real-world transport validity. Do not claim causal effects from observational forecast comparisons; interventions are controlled simulator actions.
