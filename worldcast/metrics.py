import numpy as np


def regression_metrics(y_true, y_pred):
    err = np.asarray(y_true) - np.asarray(y_pred)
    return {"mae": float(np.mean(np.abs(err))), "rmse": float(np.sqrt(np.mean(err**2)))}
