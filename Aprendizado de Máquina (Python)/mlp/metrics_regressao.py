# Métricas de avaliação para regressão.

import numpy as np


def mse(y_true, y_pred):
    # Mean Squared Error.
    return float(np.mean((y_true - y_pred) ** 2))


def rmse(y_true, y_pred):
    # Root Mean Squared Error.
    return float(np.sqrt(mse(y_true, y_pred)))


def r2_score(y_true, y_pred):
    # Coeficiente de determinação R².
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return float(1.0 - ss_res / ss_tot) if ss_tot > 0 else 0.0
