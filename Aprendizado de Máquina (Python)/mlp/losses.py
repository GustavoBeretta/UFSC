# Funções de custo com passagem direta (escalar) e reversa (gradiente).

import numpy as np


class Loss:
    # Classe base para funções de custo.

    def forward(self, y_true, y_pred):
        # Calcula o custo escalar.
        raise NotImplementedError

    def backward(self, y_true, y_pred):
        # Calcula dL/dy_pred com o fator 1/N incluído.
        raise NotImplementedError


class BinaryCrossEntropy(Loss):
    # Entropia cruzada binária: -mean(y*log(p) + (1-y)*log(1-p)).

    EPS = 1e-12

    def forward(self, y_true, y_pred):
        # Custo BCE médio sobre o batch.
        p = np.clip(y_pred, self.EPS, 1.0 - self.EPS)
        return float(-np.mean(y_true * np.log(p) + (1.0 - y_true) * np.log(1.0 - p)))

    def backward(self, y_true, y_pred):
        # Gradiente dL/dp dividido por N.
        N = y_true.shape[0]
        p = np.clip(y_pred, self.EPS, 1.0 - self.EPS)
        # Forma geral para qualquer ativação de saída: com Sigmoid simplifica para (p-y)/N.
        return (p - y_true) / (p * (1.0 - p)) / N
