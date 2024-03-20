#leitura da base de dados
library(data.table)
base <- fread(input = paste0("mobile.csv"), header = T, na.strings =
                "NA", data.table = FALSE, dec = ",")

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

# AMOSTRA SIMPLES AO ACASO
amostra400 <- base[sample(nrow(base), size=400), ]

#Analise battery_power
summary(amostra400$battery_power)
quantile(amostra400$battery_power,probs=0.05)
quantile(amostra400$battery_power,probs=0.95)

#Analise ram
summary(amostra400$ram)
quantile(amostra400$ram,probs=0.05)
quantile(amostra400$ram,probs=0.95)

library(dplyr)
battery_power_price_range <- amostra400 %>%
  group_by(price_range) %>%
  summarise(
    media = mean(battery_power),
    mediana = median(battery_power),
    percentil_5 = quantile(battery_power, 0.05),
    percentil_25 = quantile(battery_power, 0.25),
    percentil_75 = quantile(battery_power, 0.75),
    percentil_95 = quantile(battery_power, 0.95),
    minimo = min(battery_power),
    maximo = max(battery_power)
  )

ram_price_range <- amostra400 %>%
  group_by(price_range) %>%
  summarise(
    media = mean(ram),
    mediana = median(ram),
    percentil_5 = quantile(ram, 0.05),
    percentil_25 = quantile(ram, 0.25),
    percentil_75 = quantile(ram, 0.75),
    percentil_95 = quantile(ram, 0.95),
    minimo = min(ram),
    maximo = max(ram)
  )
battery_power_price_range
ram_price_range