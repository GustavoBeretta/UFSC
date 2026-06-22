# Utilitários de dados: divisão treino/teste e padronização de features

import numpy as np


def train_test_split(X, y, test_size=0.2, shuffle=True, random_state=None):
    # Divide X e y em subconjuntos de treino e teste
    N = X.shape[0]
    n_test = int(N * test_size) if isinstance(test_size, float) else int(test_size)

    if shuffle:
        idx = np.random.default_rng(random_state).permutation(N)
    else:
        idx = np.arange(N)

    train_idx, test_idx = idx[n_test:], idx[:n_test]
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]


class StandardScaler:
    # Padroniza features para média zero e variância unitária

    def __init__(self):
        self.mean_ = None
        self.std_ = None

    def fit(self, X):
        # Calcula média e desvio padrão por feature a partir de X
        self.mean_ = np.mean(X, axis=0)
        self.std_ = np.std(X, axis=0)
        # Features constantes causariam divisão por zero; substituímos por 1.
        self.std_[self.std_ == 0] = 1.0
        return self

    def transform(self, X):
        # Aplica a padronização usando as estatísticas ajustadas
        return (X - self.mean_) / self.std_

    def fit_transform(self, X):
        # Ajusta e transforma X em uma única chamada
        return self.fit(X).transform(X)
