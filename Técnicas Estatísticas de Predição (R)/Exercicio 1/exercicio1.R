#leitura da base de dados
base = read.csv2("apartamento.csv", dec=".")
base$Local = as.factor(base$Local)

#criando amostra
amostra <- base[sample(nrow(base), 80), ]

#criando modelo de regressão
modelo <- lm(Valor ~ Area + Idade + Energia + Local, data = base)
summary(modelo)

#gráficos
library (car)
qqPlot(modelo)
plot(fitted(modelo), rstandard(modelo))
abline(0,0)