# Rede MLP: organiza camadas em feedforward com retropropagação.

import numpy as np


class MLP:
    # Perceptron multicamadas: empilha camadas Dense e treina com mini-batches.

    def __init__(self):
        self.layers = []
        self.loss = None
        self.optimizer = None
        self.metric = None

    def add(self, layer):
        # Adiciona uma camada ao final da rede.
        self.layers.append(layer)

    def compile(self, loss, optimizer, metric='accuracy'):
        """Define a função de custo, o otimizador e a métrica de acompanhamento.

        metric='accuracy' mantém o comportamento original (classificação binária).
        metric=None desativa o cálculo de acurácia (use para regressão).
        """
        self.loss = loss
        self.optimizer = optimizer
        self.metric = metric

    def forward(self, x):
        # Passagem direta por todas as camadas em ordem.
        out = x
        for layer in self.layers:
            out = layer.forward(out)
        return out

    def backward(self, grad):
        # Retropropaga o gradiente por todas as camadas em ordem reversa.
        for layer in reversed(self.layers):
            grad = layer.backward(grad)

    def fit(self, X, y, epochs, batch_size=32, shuffle=True, verbose=True,
            validation_data=None):
        # Treina com gradiente descendente mini-batch e retorna histórico de métricas.
        y = y.reshape(-1, 1) if y.ndim == 1 else y
        N = X.shape[0]
        effective_bs = N if batch_size is None else batch_size

        use_accuracy = self.metric == 'accuracy'
        history = {'loss': [], 'accuracy': []} if use_accuracy else {'loss': []}
        if validation_data is not None:
            X_val, y_val = validation_data
            y_val = y_val.reshape(-1, 1) if y_val.ndim == 1 else y_val
            history['val_loss'] = []
            if use_accuracy:
                history['val_accuracy'] = []

        print_every = max(1, epochs // 20)

        for epoch in range(epochs):
            if shuffle:
                idx = np.random.permutation(N)
                X, y = X[idx], y[idx]

            for start in range(0, N, effective_bs):
                Xb = X[start:start + effective_bs]
                yb = y[start:start + effective_bs]
                y_pred = self.forward(Xb)
                self.backward(self.loss.backward(yb, y_pred))
                self.optimizer.step(self.layers)

            y_pred_full = self.forward(X)
            epoch_loss = self.loss.forward(y, y_pred_full)
            history['loss'].append(epoch_loss)

            if use_accuracy:
                if y.shape[1] == 1:
                    epoch_acc = float(
                        np.mean((y_pred_full >= 0.5).astype(int) == y.astype(int))
                    )
                else:
                    epoch_acc = float(
                        np.mean(np.argmax(y_pred_full, axis=1) == np.argmax(y, axis=1))
                    )
                history['accuracy'].append(epoch_acc)

            if validation_data is not None:
                y_vp = self.forward(X_val)
                history['val_loss'].append(self.loss.forward(y_val, y_vp))
                if use_accuracy:
                    if y_val.shape[1] == 1:
                        history['val_accuracy'].append(
                            float(np.mean((y_vp >= 0.5).astype(int) == y_val.astype(int)))
                        )
                    else:
                        history['val_accuracy'].append(
                            float(np.mean(np.argmax(y_vp, axis=1) == np.argmax(y_val, axis=1)))
                        )

            if verbose and (epoch % print_every == 0 or epoch == epochs - 1):
                msg = f"epoch {epoch:4d}  loss {epoch_loss:.4f}"
                if use_accuracy:
                    msg += f"  acc {history['accuracy'][-1]:.4f}"
                if validation_data is not None:
                    msg += f"  val_loss {history['val_loss'][-1]:.4f}"
                    if use_accuracy:
                        msg += f"  val_acc {history['val_accuracy'][-1]:.4f}"
                print(msg)

        return history

    def predict_proba(self, X):
        # Saída bruta da rede (probabilidades).
        return self.forward(X)

    def predict(self, X, threshold=0.5):
        # Predições binárias inteiras no limiar dado.
        return (self.predict_proba(X) >= threshold).astype(int)

    def evaluate(self, X, y):
        # Calcula custo e métrica de desempenho em um conjunto rotulado.
        y = y.reshape(-1, 1) if y.ndim == 1 else y
        y_pred = self.predict_proba(X)
        loss_val = self.loss.forward(y, y_pred)
        if self.metric == 'accuracy':
            if y.shape[1] == 1:
                acc = float(np.mean((y_pred >= 0.5).astype(int) == y.astype(int)))
            else:
                acc = float(np.mean(np.argmax(y_pred, axis=1) == np.argmax(y, axis=1)))
            return loss_val, acc
        return loss_val, None
