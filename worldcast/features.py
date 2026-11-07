from __future__ import annotations
import numpy as np
import pandas as pd

TARGET = "passenger_demand"


def make_supervised(frame: pd.DataFrame, lookback: int = 12, horizon: int = 1):
    """Create city-wise windows with local lags and cross-city context."""
    pivot = frame.pivot(index="time", columns="city", values=TARGET).sort_index()
    cargo = frame.pivot(index="time", columns="city", values="cargo_demand").sort_index()
    congestion = frame.pivot(index="time", columns="city", values="congestion").sort_index()
    x, y, meta = [], [], []
    values, cargo_values, cong_values = pivot.to_numpy(), cargo.to_numpy(), congestion.to_numpy()
    for t in range(lookback, len(pivot) - horizon + 1):
        for city in range(values.shape[1]):
            local = values[t-lookback:t, city]
            network = values[t-lookback:t].mean(axis=1)
            x.append(np.r_[local, network[-4:], cargo_values[t-lookback:t, city][-4:], cong_values[t-lookback:t, city][-4:]])
            y.append(values[t+horizon-1, city])
            meta.append((t, city))
    return np.asarray(x), np.asarray(y), pd.DataFrame(meta, columns=["time_index", "city"])
