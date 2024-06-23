#carregando pacotes necessários
library(car)

#lendo a base de dados
base <- read.csv('euro2024_players.csv')
summary(base)

#montando modelo de regressão múltipla
modelo <- step(lm(log(MarketValue) ~ Age + log(Height) + Foot + log(Caps+1) + Goals, data = base))

#análises do modelo
summary(modelo)
qqPlot(modelo)
plot(fitted(modelo), rstandard(modelo))
abline(0,0)