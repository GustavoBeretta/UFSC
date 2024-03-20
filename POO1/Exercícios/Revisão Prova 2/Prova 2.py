#questão 1

#pedindo o número de candidatos
while True:
    seres = int(input('Digite o número de seres que querem ser o novo godofor (mín: 1/máx: 100): '))
    if seres < 1 or seres > 100:
        print('O número de seres deve estar entre 1 e 100')
    else:
        break
inscritos = []

#pedindo o nome e poder dos candidatos
for cont in range(seres):
    candidato = {}
    candidato['Nome'], candidato['Poder'] = input('Nome e poder do candidato, respectivamente: ').split()
    while len(candidato['Nome']) < 1 or len(candidato['Nome']) > 100:
        candidato['Nome'] = input('O tamanho do nome do candidato deve ser entre 1 e 100 caracteres. Digite outro: ')
    candidato['Poder'] = int(candidato['Poder'])
    while candidato['Poder'] < 1 or candidato['Poder'] > 100:
        candidato['Poder'] = int(input('O poder do candidato deve ser entre 1 e 100. Digite novamente: '))
    inscritos.append(candidato)

#verificando o candidato com maior poder
for cont2 in range(len(inscritos)):
    if cont2 == 0:
        maiores = []
        maiores.append(inscritos[cont2])
    elif inscritos[cont2]['Poder'] > maiores[0]['Poder']:
        maiores.clear()
        maiores.append(inscritos[cont2])
    elif inscritos[cont2]['Poder'] == maiores[0]['Poder']:
        maiores.append(inscritos[cont2])
if len(maiores) == 1:
    print(maiores[0]['Nome'])

#verificando o candidato com maior poder e menor nome
else:
    for cont3 in range(len(maiores)):
        if cont3 == 0:
            menor = maiores[cont3]['Nome']
        elif len(maiores[cont3]['Nome']) < len(menor):
            menor = maiores[cont3]['Nome']
    print(menor)

'''
#questão 2

aposta = []
sorteio = []
while True:
    aposta = input('Digite a aposta de Flavinho (6 números distintos entre 1 e 99): ').split() 
    if len(aposta) != 6:
        print('A aposta deve ter 6 números')
    else:
        break
for cont in range(len(aposta)):
    aposta[cont] = int(aposta[cont])
    while aposta[cont] < 1 or aposta[cont] > 99 or aposta.count(aposta[i]) > 1:
        aposta[cont] = int(input('Os números devem ser distintos e entre 1 e 99. Digite outro: '))      
while True:
    sorteio = input('Digite os números sorteados (6 números distintos entre 1 e 99): ').split()
    if len(sorteio) != 6:
        print('O sorteio deve ter 6 números')
    else:
        break
for cont2 in range(len(sorteio)):
    sorteio[cont2] = int(sorteio[cont2])
    while sorteio[cont2] < 1 or sorteio[cont2] > 99 or sorteio.count(sorteio[i]) > 1:
        sorteio[cont2] = int(input('Os números devem ser distintos e entre 1 e 99. Digite outro: '))
acertos = 0
for cont3 in aposta:
    for cont4 in sorteio:
        if cont3 == cont4:
            acertos += 1
if acertos < 3:
    print('azar')
elif acertos == 3:
    print('terno')
elif acertos == 4:
    print('quadra')
elif acertos == 5:
    print('quina')
elif acertos == 6:
    print('sena')

#questão 3

#pedindo o tamanho da matriz:
while True:
    while True:
        linhas, colunas = input('Digite o número de linhas e colunas da matriz (mín: 1/máx: 100), respectivamente: ').split()
        linhas = int(linhas)
        colunas = int(colunas)
        if linhas == 0 and colunas == 0:
            break
        if colunas > 100 or linhas > 100 or linhas < 1 or colunas < 1:
            print('Os números de linhas e colunas devem estar entre 1 e 100')
        else:
            break
    if linhas == 0 and colunas == 0:
        break
    #criando a matriz:
    matriz = []
    for cont in range(linhas):
        linha = []
        while True:
            linha = input(f'Linha: {cont}. Para cada uma das {colunas} colunas, digite 1 se houver queijo ou 0 se não houver: ').split()
            if len(linha) != colunas:
                print(f'As linhas são compostas por {colunas} colunas')
            else:
                break
        for cont2 in range(len(linha)):
            linha[cont2] = int(linha[cont2])
            while linha[cont2] != 0 and linha[cont2] != 1:
                 linha[cont2] = int(input('Os valores aceitos são apenas 1 e 0. Digite novamente para a coluna {cont2}: '))
        matriz.append(linha)
    linha = []

    #criando o tabuleiro do jogo:
    tabuleiro = []
    for l in range(len(matriz)):
        for c in range(len(matriz[l])):
            if matriz[l][c] == 1:
                linha.append(9)
            else:
                paes = 0
                if c+1 < len(matriz[l]) and matriz[l][c+1] == 1:
                    paes += 1
                if c-1 >= 0 and matriz[l][c-1] == 1:
                    paes += 1
                if l+1 < len(matriz) and matriz[l+1][c] == 1:
                    paes += 1
                if l-1 >= 0 and matriz[l-1][c] == 1:
                    paes += 1
                linha.append(paes)
        tabuleiro.append(linha)
        linha = []
    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro[i])):
            print(tabuleiro[i][j], end='')
        print()
'''