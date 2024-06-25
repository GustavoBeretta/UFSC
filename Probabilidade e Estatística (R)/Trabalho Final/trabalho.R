#carregando a base de dados
library(data.table)
base <- fread(input = paste0("brazil_cities_2022.csv"), header = T,
              na.strings = "NA", data.table = FALSE, dec=",")
#organizando variaveis
base$IDHM <- as.numeric(base$IDHM)
base$LAT <- as.numeric(base$LAT)
base$LONG <- as.numeric(base$LONG)
#grafico posições geograficas das cidades
coordenadas <- data.frame(base$STATE, base$LONG, base$LAT, base$IDHM)
colnames(coordenadas) <- c("Estado", "Longitude", "Latitude", "IDH")
coordenadas <- subset(coordenadas, Longitude != 0)
coordenadas <- subset(coordenadas, Latitude != 0)
library(ggplot2)
ggplot(data = coordenadas, aes(Longitude, Latitude, color=Estado)) +
  geom_point()
#grafico de cidades por estado
valor_cidades_por_estado <- table(base$STATE)
valor_cidades_por_estado_ordenado <-
  valor_cidades_por_estado[order(valor_cidades_por_estado)]
tabela_cidades_por_estado <-
  data.frame(valor_cidades_por_estado_ordenado)
colnames(tabela_cidades_por_estado) <- c("Estado", "N° de cidades")
ggplot(tabela_cidades_por_estado, aes(x = Estado, y = `N° de cidades`,
                                      fill = Estado)) +
  geom_bar(stat = "identity") +
  labs(title = "N° de Cidades por Estado", x = "Estado", y = "N° de
cidades") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
#analise da população das cidades
populacao_nao_zerada <- data.frame(base$ESTIMATED_POP, base$STATE)
colnames(populacao_nao_zerada) <- c("População", "Estado")
populacao_nao_zerada <- subset(populacao_nao_zerada, População != 0)
summary(populacao_nao_zerada$População)
## Min. 1st Qu. Median Mean 3rd Qu. Max.
## 786 5454 11591 37439 25305 12176866
tabela_populacao_estados <- aggregate(População ~ Estado, data =
                                        populacao_nao_zerada, FUN = sum)
colnames(tabela_populacao_estados) <- c("Estado", "População")
tabela_populacao_estados$`N° de cidades` <- valor_cidades_por_estado
tabela_populacao_estados$`Média de população por cidade` <-
  tabela_populacao_estados$`População` / tabela_populacao_estados$`N° de
cidades`
mediana_populacao_estados <- aggregate(ESTIMATED_POP ~ STATE, data =
                                         base, FUN = median)
mediana_populacao_estados_para_tabela <- mediana_populacao_estados[,-1]
tabela_populacao_estados$`Mediana de população por cidade` <-
  mediana_populacao_estados_para_tabela
mediana_populacao_estados_semDF <-
  mediana_populacao_estados_para_tabela[-7]
boxplot(mediana_populacao_estados_semDF,
        main = "Mediana da população das cidades por estado brasileiro",
        xlab = "População",
        ylab = "",
        col = "lightblue",
        horizontal = TRUE)
#analise do fluxo de caixa das cidades e comparaçao com n° de habitantes
fluxo_caixa_cidades <- data.frame(base$ESTIMATED_POP, base$TAXES*1000,
                                  base$MUN_EXPENDIT, base$IDHM)
colnames(fluxo_caixa_cidades) <- c("População", "Impostos", "Gastos
municipais", "IDH")
fluxo_caixa_cidades <- subset(fluxo_caixa_cidades, `Gastos municipais` !=
                                0)
fluxo_caixa_cidades <- subset(fluxo_caixa_cidades, Impostos != 0)
fluxo_caixa_cidades <- subset(fluxo_caixa_cidades, População != 0)
summary(fluxo_caixa_cidades$População)
## Min. 1st Qu. Median Mean 3rd Qu. Max.
## 786 5354 11640 40951 25802 12176866
fluxo_caixa_cidades$`Grupo populacional` [fluxo_caixa_cidades$População
                                          <= 5354] <- "1"
fluxo_caixa_cidades$`Grupo populacional` [fluxo_caixa_cidades$População >
                                            5354 & fluxo_caixa_cidades$População <= 11640] <- "2"
fluxo_caixa_cidades$`Grupo populacional` [fluxo_caixa_cidades$População >
                                            11640 & fluxo_caixa_cidades$População <= 25802] <- "3"
fluxo_caixa_cidades$`Grupo populacional` [fluxo_caixa_cidades$População >
                                            25802] <- "4"
fluxo_caixa_cidades$Diferença <- fluxo_caixa_cidades$Impostos -
  fluxo_caixa_cidades$`Gastos municipais`
fluxo_caixa_cidades$Superávit [fluxo_caixa_cidades$Diferença <= 0] <-
  "Não"
fluxo_caixa_cidades$Superávit [fluxo_caixa_cidades$Diferença > 0] <-
  "Sim"
grafico_lucro <- data.frame(table(fluxo_caixa_cidades$Superávit,
                                  fluxo_caixa_cidades$`Grupo populacional`))
colnames(grafico_lucro) <- c("Superávit", "Grupo populacional", "Freq")
ggplot(grafico_lucro, aes(fill=Superávit, y=Freq, x=`Grupo
                          populacional`)) +
  geom_bar(position="fill", stat="identity") +
  ylab("Superávit?")
#IDH e população
idh_nao_zerado <- data.frame(base$ESTIMATED_POP, base$IDHM)
colnames(idh_nao_zerado) <- c("População", "IDH")
idh_nao_zerado <- subset(idh_nao_zerado, IDH != 0)
summary(idh_nao_zerado$IDH)
## Min. 1st Qu. Median Mean 3rd Qu. Max.
## 0.4180 0.5990 0.6650 0.6592 0.7180 0.8620
boxplot(idh_nao_zerado$IDH,
        main = "IDH das cidades brasileiras",
        xlab = "IDH",
        ylab = "",
        col = "lightblue",
        horizontal = TRUE)
idh_nao_zerado$`Grupo IDH` [idh_nao_zerado$IDH < 0.555] <- "Baixo"
idh_nao_zerado$`Grupo IDH` [idh_nao_zerado$IDH >= 0.555 &
                              idh_nao_zerado$IDH < 0.7] <- "Médio"
idh_nao_zerado$`Grupo IDH` [idh_nao_zerado$IDH >= 0.7 &
                              idh_nao_zerado$IDH < 0.8] <- "Alto"
idh_nao_zerado$`Grupo IDH` [idh_nao_zerado$IDH >= 0.8] <- "Muito alto"
tabela_para_grafico_grupoidh <- aggregate(População ~ `Grupo IDH`, data =
                                            idh_nao_zerado, FUN = sum)
tabela_para_grafico_grupoidh$`Grupo IDH` <-
  factor(tabela_para_grafico_grupoidh$`Grupo IDH`, levels = c("Baixo",
                                                              "Médio", "Alto", "Muito alto"))
ggplot(tabela_para_grafico_grupoidh, aes(x = `Grupo IDH`, y = População,
                                         fill = `Grupo IDH`)) +
  geom_bar(stat = "identity") +
  labs(title = "População por grupo de IDH", x = "Grupo de IDH", y =
         "População") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
#IDH e superavit
fluxo_caixa_cidades <- subset(fluxo_caixa_cidades, IDH != 0)
fluxo_caixa_cidades$`Grupo IDH` [fluxo_caixa_cidades$IDH < 0.555] <-
  "Baixo"
fluxo_caixa_cidades$`Grupo IDH` [fluxo_caixa_cidades$IDH >= 0.555 &
                                   fluxo_caixa_cidades$IDH < 0.7] <- "Médio"
fluxo_caixa_cidades$`Grupo IDH` [fluxo_caixa_cidades$IDH >= 0.7 &
                                   fluxo_caixa_cidades$IDH < 0.8] <- "Alto"
fluxo_caixa_cidades$`Grupo IDH` [fluxo_caixa_cidades$IDH >= 0.8] <-
  "Muito alto"
grafico_idh <- data.frame(table(fluxo_caixa_cidades$Superávit,
                                fluxo_caixa_cidades$`Grupo IDH`))
colnames(grafico_idh) <- c("Superávit", "Grupo IDH", "Freq")
grafico_idh$`Grupo IDH` <- factor(grafico_idh$`Grupo IDH`, levels =
                                    c("Baixo", "Médio", "Alto", "Muito alto"))
ggplot(grafico_idh, aes(fill=Superávit, y=Freq, x=`Grupo IDH`)) +
  geom_bar(position="fill", stat="identity") +
  ylab("Superávit?")
#IDH e mapa:
coordenadas$`Grupo IDH` [coordenadas$IDH < 0.555] <- "Baixo"
coordenadas$`Grupo IDH` [coordenadas$IDH >= 0.555 & coordenadas$IDH <
                           0.7] <- "Médio"
coordenadas$`Grupo IDH` [coordenadas$IDH >= 0.7 & coordenadas$IDH < 0.8]
<- "Alto"
coordenadas$`Grupo IDH` [coordenadas$IDH >= 0.8] <- "Muito alto"
coordenadas$`Grupo IDH` <- factor(coordenadas$`Grupo IDH`, levels =
                                    c("Baixo", "Médio", "Alto", "Muito alto"))
ggplot(data = coordenadas, aes(Longitude, Latitude, color=`Grupo IDH`)) +
  geom_point()