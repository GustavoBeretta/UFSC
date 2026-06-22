# Inicializador He Normal para ativações ReLU/ELU.

import numpy as np
from mlp.initializers import Initializer


class HeNormal(Initializer):
    """He Normal: N(0, sqrt(2/fan_in)).

    O rng é criado uma vez no __init__ para que duas camadas com o mesmo
    (fan_in, fan_out) nunca produzam pesos idênticos, mesmo com seed fixa.
    """

    def __init__(self, seed=None):
        super().__init__(seed=seed)
        self._rng = np.random.default_rng(seed)

    def init_weights(self, fan_in, fan_out):
        std = np.sqrt(2.0 / fan_in)
        return self._rng.normal(0.0, std, (fan_in, fan_out))

    def init_bias(self, units):
        return np.zeros((1, units))
