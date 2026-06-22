# Projeto Final: Redes Neurais 

**Integrantes da Equipe:**
- [Gustavo Beretta Gonçalves] -> usuários Códigos@UFSC: @gustavo.b.goncalves
- [Luiz Adriano Augusto dos Santos] -> usuários Códigos@UFSC: @luiz.aas
- [Rafaela Silva Borges] -> usuários Códigos@UFSC: @rafaela.s.borges

Este projeto implementa uma biblioteca de Perceptron Multicamadas (MLP) construída do zero utilizando apenas Python e NumPy. O objetivo é fornecer uma API flexível para a construção, treinamento e avaliação de redes neurais artificiais sem a dependência de frameworks de aprendizado de máquina, como TensorFlow ou PyTorch.

## Instalação

Para utilizar a biblioteca, basta clonar o repositório e instalar as dependências necessárias contidas no arquivo `requirements.txt`. Recomenda-se o uso de um ambiente virtual.

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd <nome-do-diretorio>

# Crie e ative um ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate  # No Linux/Mac
venv\Scripts\activate     # No Windows

# Instale as dependências
pip install -r requirements.txt
```

## Arquitetura da API

A biblioteca foi desenhada com uma arquitetura modular e extensível. Ela permite empilhar quantidades arbitrárias de camadas ocultas e configurar os parâmetros do treinamento instanciando classes especializadas. A principal entidade da API é a classe `MLP` que atua como um grafo de execução sequencial (Feedforward).

Os principais componentes e o fluxo de dados operam da seguinte forma:

1. **Camadas (`Dense`)**: Unidades básicas de processamento. Uma camada avalia $Z = X \cdot W + b$ e aplica uma função de ativação escalar $A = f(Z)$. Cada camada detém a capacidade de calcular o passe para a frente (`forward`) e propagar (e processar) localmente seus gradientes em relação a pesos e entradas durante o passe para trás (`backward`).
2. **Ativações (`Activation`)**: Encapsulam a não linearidade. Foram implementadas e integradas 9 funções base: `Sigmoid`, `ReLU`, `LeakyReLU`, `SELU`, `PReLU`, `ELU`, `Tanh`, `Swish` e `Softmax`. Todas provêm métodos compatíveis para uso nos passes forward/backward.
3. **Inicializadores de Pesos (`Initializer`)**: Definem a regra de geração aleatória das matrizes de pesos para quebrar a simetria inicial (foram incluídos os populares `GlorotUniform`, `GlorotNormal` e `HeNormal`).
4. **Função de Custo (`Loss`)**: Responsável por quantificar a divergência entre a saída da rede e o resultado esperado, cobrindo cenários de Regressão (`MeanSquaredError`) ou Classificação (`BinaryCrossEntropy`, `CategoricalCrossEntropy`).
5. **Otimizador (`GradientDescent`)**: Agente que atua na arquitetura atualizando sistematicamente os pesos e viéses a partir dos gradientes obtidos após o *backpropagation*.
6. **Rede (`MLP`)**: Orquestra o treinamento. 
   - `add`: Adiciona as camadas `Dense` sucessivas.
   - `compile`: Agrupa hiperparâmetros e referências fundamentais (função de custo, otimizador, métrica de desempenho).
   - `fit`: Orquestra o algoritmo de Mini-Batch Gradient Descent ao longo de múltiplas épocas, reportando logs e as perdas de treinamento/validação.
   - `evaluate` / `predict` / `predict_proba`: Realizam inferência sobre novos dados brutos.

## Uso

A API pode ser usada para problemas de classificação (binária ou multiclasse) bem como de regressão linear não-triviais. Abaixo segue um exemplo para instanciar, compilar e treinar um modelo base:

```python
import numpy as np
from mlp.activations import LeakyReLU, Sigmoid
from mlp.initializers import GlorotUniform
from mlp.layer import Dense
from mlp.losses import BinaryCrossEntropy
from mlp.network import MLP
from mlp.optimizers import GradientDescent
from mlp.utils import StandardScaler, train_test_split

# 1. Gerando dados sintéticos (dois grupos gaussianos)
rng = np.random.default_rng(0)
X = np.vstack([rng.standard_normal((100, 2)) + [-2, 0],
               rng.standard_normal((100, 2)) + [ 2, 0]])
y = np.hstack([np.zeros(100), np.ones(100)])

# 2. Pré-processamento
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 3. Construindo a rede neural
model = MLP()
model.add(Dense(8, activation=LeakyReLU(), initializer=GlorotUniform(seed=0)))
model.add(Dense(1, activation=Sigmoid(), initializer=GlorotUniform(seed=1)))

# 4. Compilando com a perda (Loss) e o Otimizador escolhido
model.compile(loss=BinaryCrossEntropy(), optimizer=GradientDescent(learning_rate=0.1), metric='accuracy')

# 5. Treinamento propriamente dito
history = model.fit(X_train, y_train, epochs=200, batch_size=32)

# 6. Avaliando o desempenho no conjunto isolado
loss, acc = model.evaluate(X_test, y_test)
print(f"Loss Final = {loss:.4f} | Acurácia Real = {acc:.4f}")
```

### Exemplos Completos (Notebooks)

Demonstrações exaustivas aplicando a biblioteca ao processamento de dados tabulares reais estão disponibilizadas no diretório `notebooks/`:
- **Classificação Binária:** `notebooks/01_binary_classification.ipynb`
- **Regressão:** `notebooks/02_regression.ipynb`
- **Classificação Multiclasse:** `notebooks/03_multiclass_classification.ipynb`

## Limitações

Apesar de robusta e coberta por validações matemáticas de retropropagação, esta biblioteca construída do zero comporta limitações ao ser comparada com plataformas empresariais robustas:
- **Ausência de suporte a Aceleração de Hardware (GPU/TPU):** As operações vetoriais delegam sua execução subjacente ao backend CPU via NumPy, restringindo o ganho de eficiência massivo provido por hardwares paralelizáveis.
- **Otimizadores Básicos:** Conta apenas com a implementação primordial do *Stochastic / Mini-Batch Gradient Descent*. Exclui recursos otimizantes contemporâneos como Adam, RMSprop ou taxas com *Momentum*.
- **Sem Regularização Embutida:** Não contemplam *Dropout* ou Penalidades de Peso Analíticas (L1/L2), exigindo mais dados para fugir do sobreajuste. 
- **Treinamento Intransigente:** Ausência do recurso analítico de *Early Stopping*, significando que o treinamento irá sempre preencher todas as épocas definidas por configuração sem parar prematuramente em caso de convergência.
