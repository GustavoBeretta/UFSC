base <- read.csv("titanic_data.csv", sep = ";")

#a)
set.seed(09092003)
amostra = base[sample(nrow(base), 300),]

#b)
amostra$Survived <- as.factor(amostra$Survived)
amostra$Pclass <- as.factor(amostra$Pclass)
amostra$Sex <- as.factor(amostra$Sex)
amostra$Embarked <- as.factor(amostra$Embarked)

#c)
modelo_inicial <- glm(Survived ~ 1, family = binomial, data = amostra)
modelo_final <- step(modelo_inicial, direction = "forward", scope = ~ Pclass + Sex + Age + SibSp + Parch + Fare + Embarked)
summary(modelo_final)

#d)
OR <- exp(coef(modelo_final))
IC <- exp(confint(modelo_final))
resultado <- data.frame(OR, IC)
print(resultado)