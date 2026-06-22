# Inicializadores de pesos para camadas Dense.

import numpy as np


class Initializer:
    # Classe base para estratégias de inicialização de pesos.

    def __init__(self, seed=None):
        self.seed = seed

    def init_weights(self, fan_in, fan_out):
        # Retorna matriz de pesos com shape (fan_in, fan_out).
        raise NotImplementedError

    def init_bias(self, units):
        # Retorna vetor de vieses com shape (1, units).
        raise NotImplementedError


class GlorotUniform(Initializer):
    # Glorot uniforme: U(-lim, lim) com lim = sqrt(6 / (fan_in + fan_out)).

    def __init__(self, seed=None):
        super().__init__(seed=seed)
        self._rng = np.random.default_rng(seed)

    def init_weights(self, fan_in, fan_out):
        # Amostra pesos de U(-lim, lim).
        limit = np.sqrt(6.0 / (fan_in + fan_out))
        return self._rng.uniform(-limit, limit, (fan_in, fan_out))

    def init_bias(self, units):
        # Retorna vieses zerados.
        return np.zeros((1, units))


class GlorotNormal(Initializer):
    # Glorot normal: N(0, std²) com std = sqrt(2 / (fan_in + fan_out)).

    def __init__(self, seed=None):
        super().__init__(seed=seed)
        self._rng = np.random.default_rng(seed)

    def init_weights(self, fan_in, fan_out):
        # Amostra pesos de uma gaussiana com variância Glorot.
        std = np.sqrt(2.0 / (fan_in + fan_out))
        return self._rng.normal(0.0, std, (fan_in, fan_out))

    def init_bias(self, units):
        # Retorna vieses zerados.
        return np.zeros((1, units))
