library(data.table)
mobile <- fread(input = paste0("mobile.csv"), header = T, na.strings = "NA",
                data.table = FALSE)

# amostra de 600 celulares
amostra <- mobile[sample(nrow(mobile), size=600), ]
coef.var <- function (variavel){
  mu <- mean(variavel, na.rm=TRUE)
  s <- sd(variavel, na.rm=TRUE)
  cv <- (s*100)/mu
  cv
}

# 1)a) média, desvio padrão e coeficiente de variação para “battery_power”, estratificada pelas categorias da variável “touch_screen”

dados_touch_0 <- amostra[amostra$touch_screen==0,]
dados_touch_0_df <-
data.frame(dados_touch_0$battery_power,dados_touch_0$touch_screen)
mean(dados_touch_0_df$dados_touch_0.battery_power)
coef.var(dados_touch_0_df$dados_touch_0.battery_power)
sd(dados_touch_0_df$dados_touch_0.battery_power)
dados_touch_1 <- amostra[amostra$touch_screen==1,]
dados_touch_1_df <-
data.frame(dados_touch_1$battery_power,dados_touch_1$touch_screen)
mean(dados_touch_1_df$dados_touch_1.battery_power)
coef.var(dados_touch_1_df$dados_touch_1.battery_power)
sd(dados_touch_1_df$dados_touch_1.battery_power)

# 1)b) média, desvio padrão e coeficiente de variação para “m_dep”, estratificada pelas categorias da variável “touch_screen”

d_m_dep_touch_0 <- amostra[amostra$touch_screen==0,]
d_m_dep_touch_0_df <-
data.frame(d_m_dep_touch_0$m_dep,d_m_dep_touch_0$touch_screen)
mean(d_m_dep_touch_0_df$d_m_dep_touch_0.m_dep)
coef.var(d_m_dep_touch_0_df$d_m_dep_touch_0.m_dep)
sd(d_m_dep_touch_0_df$d_m_dep_touch_0.m_dep)
d_m_dep_touch_1 <- amostra[amostra$touch_screen==1,]
d_m_dep_touch_1_df <-
data.frame(d_m_dep_touch_1$m_dep,d_m_dep_touch_1$touch_screen)
mean(d_m_dep_touch_1_df$d_m_dep_touch_1.m_dep)
coef.var(d_m_dep_touch_1_df$d_m_dep_touch_1.m_dep)
sd(d_m_dep_touch_1_df$d_m_dep_touch_1.m_dep)

# 1)c) média, desvio padrão e coeficiente de variação para “int_memory”, estratificada pelas categorias da variável “blue”

d_int_memory_blue_0 <- amostra[amostra$blue==0,]
d_int_memory_blue_0_df <-
  data.frame(d_int_memory_blue_0$int_memory,d_int_memory_blue_0$blue)
mean(d_int_memory_blue_0_df$d_int_memory_blue_0.int_memory)
coef.var(d_int_memory_blue_0_df$d_int_memory_blue_0.int_memory)
sd(d_int_memory_blue_0_df$d_int_memory_blue_0.int_memory)
d_int_memory_blue_1 <- amostra[amostra$blue==1,]
d_int_memory_blue_1_df <-
data.frame(d_int_memory_blue_1$int_memory,d_int_memory_blue_1$blue)
mean(d_int_memory_blue_1_df$d_int_memory_blue_1.int_memory)
coef.var(d_int_memory_blue_1_df$d_int_memory_blue_1.int_memory)
sd(d_int_memory_blue_1_df$d_int_memory_blue_1.int_memory)

# 2) gráficos de caixa do item 1
boxplot(dados_touch_0_df$dados_touch_0.battery_power,
        dados_touch_1_df$dados_touch_1.battery_power,
        names = c("Touch Screen 0", "Touch Screen 1"),
        main = "Boxplot de Battery Power para Touch Screen 0 e 1",
        ylab = "Battery Power")

boxplot(d_m_dep_touch_0_df$d_m_dep_touch_0.m_dep,
        d_m_dep_touch_1_df$d_m_dep_touch_1.m_dep,
        names = c("Touch Screen 0", "Touch Screen 1"),
        main = "Boxplot de M_Depth para Touch Screen 0 e 1",
        ylab = "M_Depth")

boxplot(d_int_memory_blue_0_df$d_int_memory_blue_0.int_memory,
        d_int_memory_blue_1_df$d_int_memory_blue_1.int_memory,
        names = c("Blue 0", "Blue 1"),
        main = "Boxplot de Int Memory para Blue 0 e 1",
        ylab = "Int Memory")