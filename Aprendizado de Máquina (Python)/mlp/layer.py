# Camada totalmente conectada (Dense).

import numpy as np
from mlp.initializers import GlorotUniform


class Dense:
    # Camada Dense: a = activation(x @ W + b), com pesos construídos preguiçosamente.

    def __init__(self, units, activation, initializer=None):
        self.units = units
        self.activation = activation
        self.initializer = initializer if initializer is not None else GlorotUniform()
        self.weights = None
        self.biases = None
        self._input = None
        self.grad_weights = None
        self.grad_biases = None

    def build(self, input_dim):
        # Aloca pesos (input_dim, units) e vieses (1, units).
        self.weights = self.initializer.init_weights(input_dim, self.units)
        self.biases = self.initializer.init_bias(self.units)

    def forward(self, x):
        # Passagem direta: constrói os pesos na primeira chamada e aplica a ativação.
        if self.weights is None:
            self.build(x.shape[1])
        self._input = x
        z = x @ self.weights + self.biases
        return self.activation.forward(z)

    def backward(self, grad_output):
        # Retropropaga o gradiente e armazena grad_weights e grad_biases para o otimizador.
        # grad_z = act'(z)*grad_out;  grad_W = x.T@grad_z;  grad_x = grad_z@W.T
        grad_z = self.activation.backward(grad_output)
        self.grad_weights = self._input.T @ grad_z
        self.grad_biases = np.sum(grad_z, axis=0, keepdims=True)
        return grad_z @ self.weights.T

    def get_params_and_grads(self):
        # Retorna [(W, dW), (b, db)] mais os parâmetros treináveis da ativação.
        pairs = [(self.weights, self.grad_weights),
                 (self.biases, self.grad_biases)]
        return pairs + self.activation.get_params_and_grads()
