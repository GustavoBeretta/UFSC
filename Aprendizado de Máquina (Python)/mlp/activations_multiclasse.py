# Ativação de saída para classificação multiclasse: Softmax

import numpy as np
from mlp.activations import Activation


class Softmax(Activation):
    """Softmax: converte logits em distribuição de probabilidade sobre C classes.

    forward : shape (N, C) -> (N, C), cada linha soma 1.
    backward: aplica o produto Jacobiana-vetor de forma eficiente (sem loop)."""

    def forward(self, z):
        # Softmax numericamente estável: subtrai max por linha antes de exp.
        self._z = z
        z_stable = z - np.max(z, axis=1, keepdims=True)
        exp_z = np.exp(z_stable)
        self._a = exp_z / np.sum(exp_z, axis=1, keepdims=True)
        return self._a

    def derivative(self, z):
        # Não utilizada diretamente — backward usa a Jacobiana vetorizada.
        raise NotImplementedError(
            "Softmax usa backward() diretamente; derivative() não se aplica."
        )

    def backward(self, grad_output):
        # Produto Jacobiana-vetor vetorizado
        # Equivale a aplicar a Jacobiana completa sem construir a matriz N x C x C.
        dot = np.sum(grad_output * self._a, axis=1, keepdims=True)
        return self._a * (grad_output - dot)
