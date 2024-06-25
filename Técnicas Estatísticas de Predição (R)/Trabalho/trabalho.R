# Carregar as bibliotecas necessárias
library(ggplot2)
library(dplyr)
library(car)

# Carregar a base de dados
data <- read.csv("euro2024_players.csv")

# Visualizar as primeiras linhas dos dados
head(data)

# Descrição dos dados
summary(data)
table(data$Foot)

# Converter a variável de mercado (MarketValue) em numérica (se não for)
data$MarketValue <- as.numeric(gsub("[^0-9]", "", data$MarketValue))

# Transformar variáveis qualitativas em fatores
data$Position <- as.factor(data$Position)

# Transformar campos vazios, "-", ou "N/A" na coluna Foot em NA
data$Foot <- ifelse(data$Foot == "" | data$Foot == "-" | data$Foot == "N/A", NA, data$Foot)
data$Foot <- as.factor(data$Foot)

# Transformar a coluna Country em fator
data$Country <- as.factor(data$Country)

# Remover linhas com valores NA na coluna Foot para as análises
data <- data[!is.na(data$Foot), ]

# Visualização inicial dos dados
# Histogramas
ggplot(data, aes(x = MarketValue)) + 
  geom_histogram(binwidth = 5000000, fill = "blue", color = "black") +
  ggtitle("Distribuição do MarketValue")

ggplot(data, aes(x = Age)) + 
  geom_histogram(binwidth = 1, fill = "green", color = "black") +
  ggtitle("Distribuição da Idade")

# Boxplots
ggplot(data, aes(x = Position, y = MarketValue)) + 
  geom_boxplot() +
  ggtitle("MarketValue por Posição")

ggplot(data, aes(x = Foot, y = MarketValue)) + 
  geom_boxplot() +
  ggtitle("MarketValue por Pé Dominante")

# Análise adicional por país
ggplot(data, aes(x = Country, y = MarketValue)) + 
  geom_boxplot() +
  ggtitle("MarketValue por País") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Análise por idade
ggplot(data, aes(x = Age, y = MarketValue)) + 
  geom_point() +
  geom_smooth(method = "lm", se = FALSE, color = "red") +
  ggtitle("MarketValue vs Idade")

# Análise por número de partidas jogadas (Caps)
ggplot(data, aes(x = Caps, y = MarketValue)) + 
  geom_point() +
  geom_smooth(method = "lm", se = FALSE, color = "red") +
  ggtitle("MarketValue vs Caps")

# Análise por número de gols marcados (Goals)
ggplot(data, aes(x = Goals, y = MarketValue)) + 
  geom_point() +
  geom_smooth(method = "lm", se = FALSE, color = "red") +
  ggtitle("MarketValue vs Goals")

# Montando modelo de regressão múltipla
modelo <- lm(log(MarketValue) ~ Age + log(Caps + 1) + log(Goals + 1) + Country + Age:log(Caps + 1) + log(Caps + 1):log(Goals + 1), data = data)

# Análises do modelo
summary(modelo)
qqPlot(modelo)
plot(fitted(modelo), rstandard(modelo))
abline(0, 0)

# Análise de influência
influencePlot(modelo)

# Diagnóstico de colinearidade
vif(modelo)