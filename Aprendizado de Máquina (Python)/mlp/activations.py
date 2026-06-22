# Funções de ativação e suas derivadas

import numpy as np


class Activation:
    # Classe base para funções de ativação.

    has_trainable_params = False

    def __init__(self):
        self._z = None

    def forward(self, z):
        # Calcula a saída da ativação e armazena z para o backward
        raise NotImplementedError

    def derivative(self, z):
        # Derivada elemento a elemento f'(z).
        raise NotImplementedError

    def backward(self, grad_output):
        # Retropropaga o gradiente pela ativação.
        return grad_output * self.derivative(self._z)

    def get_params_and_grads(self):
        # Retorna lista de pares (parâmetro, gradiente) para parâmetros treináveis.
        return []


class Sigmoid(Activation):
    # Sigmoid σ(z) = 1 / (1 + e^{-z}), implementada em dois ramos para estabilidade.

    def __init__(self):
        super().__init__()
        self._a = None

    @staticmethod
    def _sigmoid(z):
        # Ramos separados pelo sinal evitam overflow em exp().
        pos = z >= 0
        result = np.empty_like(z, dtype=float)
        result[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
        exp_z = np.exp(z[~pos])
        result[~pos] = exp_z / (1.0 + exp_z)
        return result

    def forward(self, z):
        # Calcula σ(z) e salva a saída para reutilização no backward.
        self._z = z
        self._a = self._sigmoid(z)
        return self._a

    def derivative(self, z):
        # Derivada da sigmoid: σ(z) * (1 - σ(z)).
        a = self._sigmoid(z)
        return a * (1.0 - a)

    def backward(self, grad_output):
        # Usa a saída cacheada em vez de recalcular σ(z).
        return grad_output * self._a * (1.0 - self._a)


class LeakyReLU(Activation):
    # Leaky ReLU: z se z > 0, alpha*z caso contrário (alpha fixo).

    def __init__(self, alpha=0.01):
        super().__init__()
        self.alpha = alpha

    def forward(self, z):
        # Aplica LeakyReLU e salva z.
        self._z = z
        return np.where(z > 0, z, self.alpha * z)

    def derivative(self, z):
        # Derivada do LeakyReLU.
        return np.where(z > 0, 1.0, self.alpha)


class SELU(Activation):
    # SELU auto-normalizante com constantes de Klambauer et al. (2017).

    SCALE = 1.0507009873554805
    ALPHA = 1.6732632423543772

    def forward(self, z):
        # Aplica SELU e salva z.
        self._z = z
        return np.where(z > 0, self.SCALE * z,
                        self.SCALE * self.ALPHA * (np.exp(z) - 1.0))

    def derivative(self, z):
        # Derivada do SELU.
        return np.where(z > 0, self.SCALE, self.SCALE * self.ALPHA * np.exp(z))


class PReLU(Activation):
    # PReLU: como LeakyReLU, mas alpha por unidade é aprendível via backprop.

    has_trainable_params = True

    def __init__(self, alpha_init=0.25):
        super().__init__()
        self.alpha_init = alpha_init
        self.alpha = None
        self.grad_alpha = None

    def forward(self, z):
        # Aplica PReLU, inicializando alpha na primeira chamada.
        if self.alpha is None:
            # Um alpha por unidade de saída; broadcast na dimensão do batch.
            self.alpha = np.full((1, z.shape[1]), self.alpha_init, dtype=float)
        self._z = z
        return np.where(z > 0, z, self.alpha * z)

    def derivative(self, z):
        # Derivada do PReLU em relação a z.
        return np.where(z > 0, 1.0, self.alpha)

    def backward(self, grad_output):
        # Calcula os gradientes de z e de alpha.
        grad_z = grad_output * self.derivative(self._z)
        # dL/d_alpha_j = sum_i grad[i,j] * z[i,j]  para z[i,j] <= 0
        self.grad_alpha = np.sum(
            grad_output * np.where(self._z <= 0, self._z, 0.0),
            axis=0, keepdims=True
        )
        return grad_z

    def get_params_and_grads(self):
        # Retorna alpha e seu gradiente para o otimizador.
        return [(self.alpha, self.grad_alpha)]
