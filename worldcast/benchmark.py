import pandas as pd
from .features import make_supervised
from .models import Persistence, SeasonalNaive, RidgeContext
from .metrics import regression_metrics


def run_benchmark(frame: pd.DataFrame, lookback: int = 52, train_fraction: float = .7):
    x, y, meta = make_supervised(frame, lookback=lookback)
    cut = int(meta.time_index.max() * train_fraction)
    train, test = meta.time_index.to_numpy() <= cut, meta.time_index.to_numpy() > cut
    if not train.any() or not test.any():
        raise ValueError("not enough samples for chronological split")
    models = {"persistence": Persistence(lookback), "seasonal_naive": SeasonalNaive(52), "ridge_context": RidgeContext()}
    rows = []
    for name, model in models.items():
        model.fit(x[train], y[train])
        scores = regression_metrics(y[test], model.predict(x[test]))
        rows.append({"model": name, **scores, "n_test": int(test.sum())})
    return pd.DataFrame(rows).sort_values("mae").reset_index(drop=True)
