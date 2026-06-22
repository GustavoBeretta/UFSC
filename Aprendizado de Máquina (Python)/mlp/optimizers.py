"""Otimizador de gradiente descendente."""


class GradientDescent:
    """Gradiente descendente com taxa de aprendizado fixa."""

    def __init__(self, learning_rate=0.01):
        self.learning_rate = learning_rate

    def step(self, layers):
        """Atualiza todos os parâmetros das camadas com param -= lr * grad."""
        for layer in layers:
            for param, grad in layer.get_params_and_grads():
                param -= self.learning_rate * grad

    def __repr__(self):
        return f"GradientDescent(learning_rate={self.learning_rate})"
