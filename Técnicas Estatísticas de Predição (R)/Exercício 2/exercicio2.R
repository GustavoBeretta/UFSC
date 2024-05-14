#lendo a base de dados
base <- read.csv("car_base.csv", sep=";")

#a) retirando as observações "drivewheel=4wd"
base <- subset(base, drivewheel != "4wd")

#b) retirando a amostra
set.seed(09092003)
base = base[sample(nrow(base), 120),]

#c) ajuste do modelo
modelo <- lm(price ~ carwidth * drivewheel, data = base)

#d) análise do modelo
summary(modelo)

#e) gráfico
library(ggplot2)
ggplot(base, aes(x = carwidth, y = price, color = drivewheel)) +
  geom_point() +
  stat_smooth(method = "lm", se = FALSE) +
  labs(title = "Interação entre Carwidth e Drivewheel no Preço",
       x = "Carwidth (polegadas)",
       y = "Price (x1000$)",
       color = "Drivewheel")

#f) intervalos
dados <- data.frame(carwidth = 70, drivewheel = "fwd")
predict(modelo, dados, interval = "confidence")
predict(modelo, dados, interval = "prediction")