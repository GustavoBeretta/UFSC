from baralho import Baralho
from jogo import Jogo
from jogador import Jogador

novo_jogo = 'S'

while True:
    n_jogadores = int(input('Digite o número de jogadores nessa partida (mínimo: 2/máximo: 8): '))
    if n_jogadores < 2 or n_jogadores > 8:
        print('O NÚMERO DE JOGADORES DEVE ESTAR ENTRE 2 E 8')
        print()
    else:
        break
while True:
    print()
    blind = int(input('Digite o valor do blind na partida (deve ser positivo e par): '))
    if blind < 1 or blind % 2 != 0:
        print('O VALOR DO BLIND DEVE SER POSITIVO E PAR')
    else:
        break
while True:
    print()
    fichas = int(input('Digite o valor de fichas que os jogadores terão no início do jogo (mínimo igual ao blind): '))
    if fichas < blind:
        print('O NÚMERO DE FICHAS DEVE SER PELO MENOS IGUAL AO BLIND')
    else:
        break

baralho = Baralho()
jogo = Jogo(blind, baralho.pegar_carta_aleatoria(), baralho.pegar_carta_aleatoria(), baralho.pegar_carta_aleatoria(), baralho.pegar_carta_aleatoria(), baralho.pegar_carta_aleatoria())
jogadores = []
print()
for cont in range(n_jogadores):
    nome = input(f'Digite o nome do jogador {cont+1}: ')
    jogador = Jogador(nome, fichas, baralho.pegar_carta_aleatoria(), baralho.pegar_carta_aleatoria())
    jogadores.append(jogador)
jogador = jogadores[0]
jogador.set_funcao('Small Blind')
jogador = jogadores[1]
jogador.set_funcao('Big Blind')

while novo_jogo == 'S':

    for rodada in range(4):
        
        if rodada == 1:
            jogo.virar_carta_um()
            jogo.virar_carta_dois()
            jogo.virar_carta_tres()
        elif rodada == 2:
            jogo.virar_carta_quatro()
        elif rodada == 3:
            jogo.virar_carta_cinco()
        
        equivalencia = False
        maior_aposta = 0
        for i in range(len(jogadores)):
            jogador = jogadores[i]
            jogador.zerar_aposta()
        
        check = 0
        
        while equivalencia == False:
            
            if check == n_jogadores:
                break
            
            for i in range(len(jogadores)):
                jogador = jogadores[i]
                
                if check == n_jogadores:
                    break
                
                for index in range(len(jogadores)):
                    player = jogadores[index]
                    if player.get_status():
                        if player.get_aposta() > maior_aposta:
                            maior_aposta = player.get_aposta()
                
                diferentes = 0
                for index in range(len(jogadores)):
                    player = jogadores[index]
                    if player.get_status():
                        if player.get_aposta() != maior_aposta or maior_aposta == 0:
                            diferentes += 1
                if diferentes == 0:
                    equivalencia = True
                
                if jogador.get_status() and (maior_aposta == 0 or jogador.get_aposta() < maior_aposta):
                    
                    print()
                    print('-----------------------------------------------------------------------------------------------------')
                    print()
                    
                    print(f'RODADA DE APOSTA {rodada+1} DE 4')
                    print(f'VEZ DO JOGADOR: {jogador.get_nome()}')
                    
                    print()
                    print('------------------------------------')
                    print()
                    
                    print(f'CARTA 1 DO JOGADOR: {jogador.get_carta_um()}')
                    print(f'CARTA 2 DO JOGADOR: {jogador.get_carta_dois()}')
                    print(f'FICHAS DO JOGADOR: {jogador.get_fichas()}')
                    print(f'APOSTA DO JOGADOR: {jogador.get_aposta()}')
                    
                    print()
                    print('------------------------------------')
                    print()
                    
                    if jogo.get_carta_um_status():
                        print(f'CARTA 1 DA MESA: {jogo.get_carta_um()}')
                    if jogo.get_carta_dois_status():
                        print(f'CARTA 2 DA MESA: {jogo.get_carta_dois()}')
                    if jogo.get_carta_tres_status():
                        print(f'CARTA 3 DA MESA: {jogo.get_carta_tres()}')
                    if jogo.get_carta_quatro_status():
                        print(f'CARTA 4 DA MESA: {jogo.get_carta_quatro()}')
                    if jogo.get_carta_cinco_status():
                        print(f'CARTA 5 DA MESA: {jogo.get_carta_cinco()}')
                    print(f'VALOR NA MESA: {jogo.get_valor_mesa()}')
                    
                    print()
                    print('------------------------------------')
                    
                    for index in range(len(jogadores)):
                        player = jogadores[index]
                        if player.get_status():
                            if player == jogador:
                                pass
                            else:
                                print()
                                print(f'FICHAS DO JOGADOR {player.get_nome()}: {player.get_fichas()}')
                                print(f'APOSTA DO JOGADOR {player.get_nome()}: {player.get_aposta()}')
                                if player.get_funcao() != 'Nada':
                                    print(f'FUNÇÃO DO JOGADOR {player.get_nome()}: {player.get_funcao()}')
                                
                    print()
                    print('------------------------------------')
                    print()
                    
                    if rodada == 0 and jogador.get_funcao() == ('Small Blind') and jogador.get_aposta() == 0:
                        input(f'O jogador {jogador.get_nome()} é o Small Blind, então sua aposta é automática. Digite qualquer coisa para prosseguir: ')
                        jogador.apostar(blind/2)
                        jogo.apostar(blind/2)
                    elif rodada == 0 and jogador.get_funcao() == ('Big Blind') and jogador.get_aposta() == 0:
                        input(f'O jogador {jogador.get_nome()} é o Big Blind, então sua aposta é automática. Digite qualquer coisa para prosseguir: ')
                        jogador.apostar(blind)
                        jogo.apostar(blind)
                    else:
                        print('Opções:')
                        print()
                        print('1 - Sair da rodada')
                        print('2 - Apostar')
                        if jogador.get_aposta() == maior_aposta:
                            print('3 - Dar check')
                            terceira_opcao = True
                        
                        while True:
                            print()
                            escolha = int(input('Digite a opção escolhida: '))
                            if escolha < 1 and escolha > 3 and terceira_opcao:
                                print('AS OPÇÕES SÃO 1, 2 e 3')
                            elif escolha != 1 and escolha != 2 and terceira_opcao == False:
                                print('AS OPÇÕES SÃO 1 e 2')
                            else:
                                break
                        
                        if escolha == 1:
                            jogador.sair()
                            
                        elif escolha == 2:
                            while True:
                                print()
                                aposta = int(input('Digite quantas fichas você deseja apostar: '))
                                if aposta < 1 or aposta > jogador.get_fichas() or aposta < (maior_aposta - jogador.get_aposta()):
                                    if aposta < 1 or aposta > jogador.get_fichas():
                                        print('O NÚMERO DE FICHAS DEVE ESTAR ENTRE 1 E A QUANTIDADE QUE VOCÊ TEM')
                                    if aposta < (maior_aposta - jogador.get_aposta()):
                                        print('VOCÊ DEVE, NO MÍNIMO, COBRIR A MAIOR APOSTA ATUAL')
                                else:
                                    break
                            jogador.apostar(aposta)
                            jogo.apostar(aposta)
                        
                        else:
                            check += 1
                            
    print()
    print('-----------------------------------------------------------------------------------------------------')
    print()
    print('APOSTAS ENCERRADAS')
    print()
    print(f'VALOR NA MESA: {jogo.get_valor_mesa()}')
    print()
    print(f'CARTA 1 DA MESA: {jogo.get_carta_um()}')
    print(f'CARTA 2 DA MESA: {jogo.get_carta_dois()}')
    print(f'CARTA 3 DA MESA: {jogo.get_carta_tres()}')
    print(f'CARTA 4 DA MESA: {jogo.get_carta_quatro()}')
    print(f'CARTA 5 DA MESA: {jogo.get_carta_cinco()}')
    print()
    print('------------------------------------')
    for index in range(len(jogadores)):
        player = jogadores[index]
        if player.get_status():
            print()
            print(f'CARTA 1 DO JOGADOR {player.get_nome()}: {player.get_carta_um()}')
            print(f'CARTA 2 DO JOGADOR {player.get_nome()}: {player.get_carta_dois()}')
    print()
    print('------------------------------------')
    print()

    for index in range(len(jogadores)):
        player = jogadores[index]
        if player.get_status():
            while True:
                ganhos = int(input(f'Digite quantas fichas o jogador {player.get_nome()} ganhou: '))
                if ganhos < 0 or ganhos > jogo.get_valor_mesa():
                    print('O VALOR NÃO PODE SER NEGATIVO E NEM MAIOR QUE O VALOR NA MESA')
                    print()
                else:
                    break
            player.ganhar(ganhos)

    while True:
        novo_jogo = input('Deseja jogar mais uma partida ("S" ou "N"): ').upper()
        if novo_jogo != 'S' and novo_jogo != 'N':
            print('AS OPÇÕES SÃO "S" E "N"')
        else:
            break

    if novo_jogo == 'S':
        baralho = Baralho()
        jogo = Jogo(blind, baralho.pegar_carta_aleatoria(), baralho.pegar_carta_aleatoria(), baralho.pegar_carta_aleatoria(), baralho.pegar_carta_aleatoria(), baralho.pegar_carta_aleatoria())
        zerados = []
        for index in range(len(jogadores)):
            player = jogadores[index]
            if player.get_fichas() == 0:
                zerados.append(player)
                pass
            player.entrar()
            player.zerar_aposta()
            player.set_funcao('Nada')
            player.set_carta_um(baralho.pegar_carta_aleatoria())
            player.set_carta_dois(baralho.pegar_carta_aleatoria())
        for player in zerados:
            jogadores.remove(player)
        small = jogadores[0]
        del jogadores[0]
        jogadores.append(small)
        jogador = jogadores[0]
        jogador.set_funcao('Small Blind')
        jogador = jogadores[1]
        jogador.set_funcao('Big Blind')
