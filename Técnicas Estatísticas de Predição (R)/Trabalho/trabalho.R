options(max.print = 1000)

#carregando pacotes necessários
library(car)

#lendo a base de dados
base <- read.csv('euro2024_players.csv')
summary(base)

#montando modelo de regressão múltipla
modelo <- step(lm(log(MarketValue) ~ Age + Club + log(Caps+1) + log(Goals+1) + Country + Age:log(Caps+1) + log(Caps+1):log(Goals+1), data = base))

#análises do modelo
sink("summary_output.txt")
summary(modelo)
sink()
qqPlot(modelo)
plot(fitted(modelo), rstandard(modelo))
abline(0,0)

