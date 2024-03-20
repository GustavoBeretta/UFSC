#leitura da base de dados
library(data.table)
base <- fread(input = paste0("mobile.csv"), header = T, na.strings =
                "NA", data.table = FALSE, dec = ",")

#ajuste de variaveis quantitativas e qualitativas
library(dplyr)

base$blue <- recode(base$blue,`0`="1: Não",`1`="2: Sim")
base$clock_speed <- as.numeric(base$clock_speed)
base$dual_sim <- recode(base$dual_sim,`0`="1: Não",`1`="2: Sim")
base$four_g <- recode(base$four_g,`0`="1: Não",`1`="2: Sim")
base$m_dep <- as.numeric(base$m_dep)
base$touch_screen <- recode(base$touch_screen,`0`="1: Não",`1`="2: Sim")
base$wifi <- recode(base$wifi,`0`="1: Não",`1`="2: Sim")
base$price_range <- recode(base$price_range,`0`="1: Baixo",`1`="2:
Médio", `2` ="3: Caro", `3` ="4: Muito Caro")

#tabela de faixa de preço
precos.freq <- table(base$price_range, useNA = "ifany")
precos.porc <- round(prop.table(precos.freq)*100,1)
precos.tabela <- data.frame(precos.porc)
colnames(precos.tabela) <- c("Faixa de preço","Porcentagem")
precos.tabela

#grafico de faixa de preço
png(file = "grafico_precos.png")
grafico_precos <- barplot(height=precos.tabela$Porcentagem,
                          names=precos.tabela$`Faixa de preço`,
                          col=rgb(0.3,0.6,0.5,0.5),
                          xlab="Faixa de preço",
                          ylab="Porcentagem",
                          main="")
dev.off()

#gráfico de relação entre wifi e preço
wifi_x_preco.tabela <- data.frame(table(base$price_range,base$wifi))
colnames(wifi_x_preco.tabela) <- c("Faixa_de_preco","WiFi","Frequencia")
library(ggplot2)
ggplot(wifi_x_preco.tabela, aes(fill=WiFi, y=Frequencia,
                                x=Faixa_de_preco)) +
  geom_bar(position="fill", stat="identity") +
  ylab("Porcentagem")

#tabela de relação entre memória RAM e preço
ram_x_preco.tabela <- aggregate(base$ram, by=list(base$price_range),
                                FUN="mean")
colnames(ram_x_preco.tabela) <- c("Faixa de preço","Memória RAM")
ram_x_preco.tabela

#classificação por memória RAM
library(psych)
base$Grupo_Ram[base$ram <800] = "G1"
base$Grupo_Ram[base$ram >=800 & base$ram <1600] = "G2"
base$Grupo_Ram[base$ram >=1600 & base$ram <2400] = "G3"
base$Grupo_Ram[base$ram >=2400 & base$ram <3200] = "G4"
base$Grupo_Ram[base$ram >=3200] = "G5"
grupos_ram <- table(base$Grupo_Ram, useNA = "ifany")
grupos_ram