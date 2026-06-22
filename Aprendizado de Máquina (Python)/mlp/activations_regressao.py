#Ativações para regressão: ReLU, Tanh, ELU, Swish, Identity.

import numpy as np
from mlp.activations import Activation


class ReLU(Activation):
    #ReLU: max(0, z).

    def forward(self, z):
        self._z = z
        return np.maximum(0.0, z)

    def derivative(self, z):
        return (z >= 0).astype(float)


class Tanh(Activation):
    #Tanh estável por ramos: evita overflow para |z| grande.

    def __init__(self):
        super().__init__()
        self._tanh = None

    @staticmethod
    def _stable_tanh(z):
        res = np.empty_like(z, dtype=float)
        pos = z >= 0
        e2p = np.exp(-2.0 * z[pos])
        res[pos] = (1.0 - e2p) / (1.0 + e2p)
        e2n = np.exp(2.0 * z[~pos])
        res[~pos] = (e2n - 1.0) / (e2n + 1.0)
        return res

    def forward(self, z):
        self._z = z
        self._tanh = self._stable_tanh(z)
        return self._tanh

    def derivative(self, z):
        if self._tanh is not None and np.array_equal(self._z, z):
            return 1.0 - self._tanh ** 2
        return 1.0 - self._stable_tanh(z) ** 2


class ELU(Activation):
    #ELU: z se z > 0, alpha*(e^z - 1) caso contrário.

    def __init__(self, alpha=1.0):
        super().__init__()
        self.alpha = alpha

    def forward(self, z):
        self._z = z
        out = np.empty_like(z, dtype=float)
        pos = z > 0
        out[pos] = z[pos]
        out[~pos] = self.alpha * (np.exp(z[~pos]) - 1.0)
        return out

    def derivative(self, z):
        out = np.empty_like(z, dtype=float)
        pos = z > 0
        out[pos] = 1.0
        out[~pos] = self.alpha * np.exp(z[~pos])
        return out


class Swish(Activation):
    #Swish: z * sigmoid(z) = z / (1 + e^{-z}).

    def __init__(self):
        super().__init__()
        self._sig = None
        self._swish = None

    def forward(self, z):
        self._z = z
        self._sig = 1.0 / (1.0 + np.exp(-z))
        self._swish = z * self._sig
        return self._swish

    def derivative(self, z):
        # swish'(z) = swish(z) + sigmoid(z) * (1 - swish(z))
        return self._swish + self._sig * (1.0 - self._swish)


class Identity(Activation):
    # Identity: f(z) = z. Usada na camada de saída para regressão.

    def forward(self, z):
        self._z = z
        return z

    def derivative(self, z):
        return np.ones_like(z)
