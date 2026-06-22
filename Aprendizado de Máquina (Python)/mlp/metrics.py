"""Métricas de avaliação para classificação binária e multiclasse."""

import numpy as np


def accuracy_score(y_true, y_pred):
    """Fração de rótulos previstos corretamente."""
    return float(np.mean(y_true.flatten() == y_pred.flatten()))


def confusion_matrix(y_true, y_pred):
    """
    Computa a matriz de confusão para avaliar a precisão da classificação.
    Suporta classificação binária e multiclasse.
    A matriz C é tal que C[i, j] é igual ao número de amostras reais no grupo i, mas preditas no grupo j.
    """
    yt = y_true.flatten().astype(int)
    yp = y_pred.flatten().astype(int)
    
    # Determina o número de classes a partir dos maiores rótulos
    num_classes = max(np.max(yt), np.max(yp)) + 1
    
    cm = np.zeros((num_classes, num_classes), dtype=int)
    for t, p in zip(yt, yp):
        cm[t, p] += 1
        
    return cm


def precision_recall_f1(y_true, y_pred):
    """Precisão, recall e F1 para classificação binária; divisão por zero retorna 0.0."""
    cm = confusion_matrix(y_true, y_pred)
    tp = cm[1, 1]
    fp = cm[0, 1]
    fn = cm[1, 0]
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    denom = precision + recall
    f1 = 2.0 * precision * recall / denom if denom > 0.0 else 0.0
    return float(precision), float(recall), float(f1)
