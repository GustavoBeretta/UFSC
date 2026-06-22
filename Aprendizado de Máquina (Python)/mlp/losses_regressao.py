# Função de custo para regressão: Mean Squared Error.

import numpy as np
from mlp.losses import Loss


class MeanSquaredError(Loss):
    # MSE: mean((y_true - y_pred)^2), gradiente com fator 1/N.

    def forward(self, y_true, y_pred):
        # Custo escalar MSE.
        return float(np.mean((y_true - y_pred) ** 2))

    def backward(self, y_true, y_pred):
        # Gradiente dL/dy_pred = 2*(y_pred - y_true) / N.
        n = y_true.shape[0]
        return 2.0 * (y_pred - y_true) / n
