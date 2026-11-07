from sklearn.linear_model import Ridge


class Persistence:
    def __init__(self, lookback: int = 52):
        self.lookback = lookback

    def fit(self, x, y):
        return self

    def predict(self, x):
        return x[:, self.lookback - 1]


class SeasonalNaive:
    def __init__(self, seasonal_period: int = 52):
        self.seasonal_period = seasonal_period

    def fit(self, x, y):
        return self

    def predict(self, x):
        return x[:, -self.seasonal_period]


class RidgeContext:
    def __init__(self, alpha: float = 10.0):
        self.model = Ridge(alpha=alpha)

    def fit(self, x, y):
        self.model.fit(x, y)
        return self

    def predict(self, x):
        return self.model.predict(x)
