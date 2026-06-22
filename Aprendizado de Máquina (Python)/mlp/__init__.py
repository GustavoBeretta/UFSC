"""Biblioteca MLP — perceptron multicamadas do zero com NumPy."""

from mlp.activations import Activation, Sigmoid, LeakyReLU, SELU, PReLU
from mlp.activations_regressao import ReLU, Tanh, ELU, Swish, Identity
from mlp.activations_multiclasse import Softmax
from mlp.losses import Loss, BinaryCrossEntropy
from mlp.losses_regressao import MeanSquaredError
from mlp.losses_multiclasse import CategoricalCrossEntropy
from mlp.initializers import Initializer, GlorotUniform, GlorotNormal
from mlp.initializers_regressao import HeNormal
from mlp.layer import Dense
from mlp.optimizers import GradientDescent
from mlp.network import MLP
from mlp.metrics import accuracy_score, confusion_matrix, precision_recall_f1
from mlp.metrics_regressao import mse, rmse, r2_score
from mlp.utils import train_test_split, StandardScaler

__all__ = [
    # ativações (classificação)
    "Activation", "Sigmoid", "LeakyReLU", "SELU", "PReLU",
    # ativações (regressão)
    "ReLU", "Tanh", "ELU", "Swish", "Identity",
    # ativações (multiclasse)
    "Softmax",
    # perdas
    "Loss", "BinaryCrossEntropy", "MeanSquaredError", "CategoricalCrossEntropy",
    # inicializadores
    "Initializer", "GlorotUniform", "GlorotNormal", "HeNormal",
    # camada e rede
    "Dense", "GradientDescent", "MLP",
    # métricas (classificação)
    "accuracy_score", "confusion_matrix", "precision_recall_f1",
    # métricas (regressão)
    "mse", "rmse", "r2_score",
    # utilitários
    "train_test_split", "StandardScaler",
]
