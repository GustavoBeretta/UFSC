# Função de custo para classificação multiclasse: Categorical Cross-Entropy

import numpy as np
from mlp.losses import Loss


class CategoricalCrossEntropy(Loss):
    """Entropia cruzada categórica:

    Espera y_true em one-hot, shape (N, C).
    Espera y_pred com probabilidades (saída do Softmax), shape (N, C)."""

    EPS = 1e-12

    def forward(self, y_true, y_pred):
        # Custo escalar CCE médio sobre o batch
        p = np.clip(y_pred, self.EPS, 1.0)
        return float(-np.mean(np.sum(y_true * np.log(p), axis=1)))

    def backward(self, y_true, y_pred):
        """Gradiente dL/dy_pred com fator 1/N.

        Combinado com Softmax no backward, simplifica para (y_pred - y_true) / N,
        mas aqui retornamos a forma geral para manter a separação de responsabilidades."""
        n = y_true.shape[0]
        p = np.clip(y_pred, self.EPS, 1.0)
        return -y_true / (p * n)
