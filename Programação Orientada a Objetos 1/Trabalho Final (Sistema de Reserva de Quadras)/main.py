from quadra import Quadra
from socio import Socio
from nao_socio import Nao_socio
from reserva import Reserva

quadras = {}
clientes = {}
reservas = {}

while True:
    print('='*70)
    print(' '*28 + 'MENU DO SISTEMA')
    print()
    print('OPERAÇÕES: ')
    print()
    print('(1) Gerenciar quadras')
    print('(2) Gerenciar clientes')
    print('(3) Gerenciar reservas')
    print()
    op1 = int(input('Digite o número correspondente à operação a ser realizada: '))
    print()
    
    if op1 < 1 or op1 > 3:
        print('='*70)
        print()
        print('OPÇÃO INDISPONÍVEL')
        print()
        
    elif op1 == 1:
        while True:
            print('='*70)
            print()
            print('GERENCIAMENTO DE QUADRAS')
            print()
            print('OPÇÕES:')
            print()
            print('(1) Cadastrar nova quadra')
            print('(2) Excluir uma quadra')
            print('(3) Consultar quadras')
            print('(4) Voltar ao menu inicial')
            print()
            op2 = int(input('Digite o número correspondente à opção desejada: '))
            print()
        
            if op2 < 1 or op2 > 4:
                print('='*70)
                print()
                print('OPÇÃO INDISPONÍVEL')
                print()
                
            elif op2 == 1:
                print('='*70)
                print()
                print('CADASTRO DE QUADRAS:')
                print()
                while True:
                    
                    while True:
                        n_identificacao = int(input('Digite um número de identificação para a quadra (não pode ser 0): '))
                        if n_identificacao in quadras:
                            print('JÁ HÁ UMA QUADRA COM ESTE NÚMERO DE IDENTIFICAÇÃO')
                            print()
                        elif n_identificacao == 0:
                            print('O NÚMERO DE IDENTIFICAÇÃO NÃO PODE SER 0')
                            print()
                        else:
                            break
                        
                    esporte = input('Digite o esporte para qual a prática na quadra é adequada: ')
                    
                    while True:
                        valor_h = float(input('Digite o valor em Reais da hora da reserva da quadra: '))
                        if valor_h < 1:
                            print('O VALOR DEVE SER IGUAL OU MAIOR A 1 REAL')
                            print()
                        else:
                            break
                        
                    while True:
                        capacidade_max = int(input('Digite a capacidade máxima de jogadores na quadra: '))
                        if capacidade_max < 1:
                            print('A CAPACIDADE MÁXIMA DEVE SER IGUAL OU MAIOR A 1 JOGADOR')
                            print()
                        else:
                            break
                        
                    while True:
                        cobertura = input('Digite se a quadra tem cobertura (S/N): ').upper()
                        if cobertura != 'S' and cobertura != 'N':
                            print('AS OPÇÕES POSSÍVEIS SÃO "S" E "N"')
                            print()
                        else:
                            break
                    
                    print()
                    print(f'NÚMERO DE IDENTIFICAÇÃO: {n_identificacao}')
                    print(f'ESPORTE: {esporte}')
                    print(f'VALOR DA HORA DE RESERVA: {valor_h} Reais')
                    print(f'CAPACIDADE MÁXIMA DE JOGADORES: {capacidade_max}')
                    print(f'COBERTURA: {cobertura}')
                    
                    while True:
                        print()
                        cadastrar = input('Deseja cadastrar esta quadra? Digite "S" ou "N": ').upper()
                        if cadastrar != 'S' and cadastrar != 'N':
                            print('AS OPÇÕES POSSÍVEIS SÃO "S" E "N"')    
                        else:
                            break
                    
                    if cadastrar == 'S':
                        quadra = Quadra(n_identificacao, esporte, valor_h, capacidade_max, cobertura)
                        quadras[n_identificacao] = quadra
                        print()
                        print(f'QUADRA {n_identificacao} CADASTRADA')
                        print()
                        print('='*70)
                    
                    while True:
                        print()
                        nova_quadra = input('Deseja cadastrar uma nova quadra? Digite "S" ou "N": ').upper()
                        if nova_quadra != 'S' and nova_quadra != 'N':
                            print('AS OPÇÕES POSSÍVEIS SÃO "S" E "N"')    
                        else:
                            break
                    
                    print()
                    
                    if nova_quadra == 'N':
                        break

            elif op2 == 2:
                print('='*70)
                print()
                print('EXCLUSÃO DE QUADRAS:')
                print()
                
                while True:
                    n_identificacao = int(input('Digite o número de identificação da quadra que deseja excluir (digite 0 para sair): '))
                    
                    if n_identificacao in quadras:
                        while True:
                            print()
                            excluir = input(f'Deseja mesmo excluir a quadra {n_identificacao}? Digite "S" ou "N": ').upper()
                            if excluir != 'S' and excluir != 'N':
                                print('AS OPÇÕES POSSÍVEIS SÃO "S" E "N"')    
                            else:
                                print()
                                break
                            
                        if excluir == 'S':
                            del quadras[n_identificacao]
                            print(f'QUADRA {n_identificacao} EXCLUÍDA')
                            print()
                            print('='*70)
                            print()
                        
                    elif n_identificacao == 0:
                        break
                    
                    else:
                        print('NÃO HÁ NENHUMA QUADRA CADASTRADA COM ESTE NÚMERO DE IDENTIFICAÇÃO')
                        print()

            elif op2 == 3:
                print('='*70)
                print()
                print('LISTA DE QUADRAS DISPONÍVEIS:')
                print()
                print('-'*70)
                print()
                
                for n_identificacao in quadras:
                    quadra = quadras[n_identificacao]
                    print('QUADRA NÚMERO:', quadra.get_n_identificacao())
                    print()
                    print('ESPORTE:', quadra.get_esporte())
                    print('VALOR DA HORA DE RESERVA:', quadra.get_valor_h(), 'Reais')
                    print('CAPACIDADE MÁXIMA DE JOGADORES:', quadra.get_capacidade_max())
                    print('COBERTURA:', quadra.get_cobertura())
                    print()
                    print('-'*70)
                    print()
                    
                print('OPÇÕES: ')
                print()
                print('(1) Alterar dados de uma quadra')
                print('(2) Voltar ao menu anterior')
                print()
                
                while True:
                    op3 = int(input('Escolha uma opção: '))
                    if op3 != 1 and op3 != 2:
                        print('As opções são "1" e "2"')
                    else:
                        break
                
                print()
                
                if op3 == 1:
                    print('='*70)
                    print()
                    print('ALTERAÇÃO DE DADOS DE UMA QUADRA:')
                    
                    while True:
                        print()
                        n_identificacao = int(input('Digite o número de identificação da quadra que você deseja alterar (digite 0 para sair): '))
                        
                        if n_identificacao in quadras:
                            quadra = quadras[n_identificacao]
                            
                            print()
                            print('OPÇÕES:')
                            print()
                            print('(1) NÚMERO DE IDENTIFICAÇÃO')
                            print('(2) ESPORTE')
                            print('(3) VALOR DA HORA DA RESERVA')
                            print('(4) CAPACIDADE MAXIMA DE JOGADORES EM QUADRA')
                            print('(5) COBERTURA')
                            print('(6) VOLTAR AO MENU ANTERIOR')
                            print()
                          
                            while True:
                                op4 = int(input('Escolha uma opção: '))
                                if op4 < 1 or op4 > 6:
                                    print('OPÇÃO INDISPONÍVEL')
                                    print()
                                else:
                                    break
                                    
                            if op4 == 1:
                                print()
                                n_antigo = n_identificacao
                                while True:
                                    n_identificacao = int(input('Digite o novo número de identificação da quadra (não pode ser 0): '))
                                    if n_identificacao in quadras:
                                        print('JÁ HÁ UMA QUADRA COM ESTE NÚMERO DE IDENTIFICAÇÃO')
                                        print()
                                    elif n_identificacao == 0:
                                        print('O NÚMERO DE IDENTIFICAÇÃO NÃO PODE SER 0')
                                        print()
                                    else:
                                        break
                                quadra.set_n_identificacao(n_identificacao)
                                quadras[n_identificacao] = quadra
                                del quadras[n_antigo]
                                print()
                                print('NÚMERO DE IDENTIFICAÇÃO ALTERADO COM SUCESSO')
                                print()
                                print('-'*70)
                                
                            elif op4 == 2:
                                print()
                                esporte = input('Digite o esporte para qual a prática na quadra é adequada: ')
                                quadra.set_esporte(esporte)
                                print()
                                print('ESPORTE ALTERADO COM SUCESSO')
                                print()
                                print('-'*70)
                            
                            elif op4 == 3:
                                while True:
                                    print()
                                    valor_h = float(input('Digite o valor em Reais da hora da reserva da quadra: '))
                                    if valor_h < 1:
                                        print('O VALOR DEVE SER IGUAL OU MAIOR A 1 REAL')
                                    else:
                                        break
                                quadra.set_valor_h(valor_h)
                                print()
                                print('VALOR DA HORA DA RESERVA ALTERADO COM SUCESSO')
                                print()
                                print('-'*70)
                                
                            elif op4 == 4:
                                while True:
                                    print()
                                    capacidade_max = int(input('Digite a capacidade máxima de jogadores na quadra: '))
                                    if capacidade_max < 1:
                                        print('A CAPACIDADE MÁXIMA DEVE SER IGUAL OU MAIOR A 1 JOGADOR')
                                    else:
                                        break
                                quadra.set_capacidade_max(capacidade_max)
                                print()
                                print('A CAPACIDADE MÁXIMA DE JOGADORES NA QUADRA FOI ALTERADA COM SUCESSO')
                                print()
                                print('-'*70)
                            
                            elif op4 == 5:
                                while True:
                                    print()
                                    cobertura = input('Digite se a quadra tem cobertura (S/N): ').upper()
                                    if cobertura != 'S' and cobertura != 'N':
                                        print('AS OPÇÕES POSSÍVEIS SÃO "S" E "N"')
                                    else:
                                        break
                                quadra.set_cobertura(cobertura)
                                print()
                                print('A COBERTURA FOI ALTERADA COM SUCESSO')
                                print()
                                print('-'*70)
                            
                            elif op4 == 6:
                                print()
                                break
                                
                        elif n_identificacao == 0:
                            print()
                            break
                            
                        else:
                            print('NÃO HÁ NENHUMA QUADRA CADASTRADA COM ESTE NÚMERO DE IDENTIFICAÇÃO')
                            
            else:
                break
            
    elif op1 == 2:
        while True:
            print('='*70)
            print()
            print('GERENCIAMENTO DE CLIENTES')
            print()
            print('OPÇÕES:')
            print()
            print('(1) Cadastrar novo cliente')
            print('(2) Excluir um cliente')
            print('(3) Consultar clintes')
            print('(4) Voltar ao menu inicial')
            print()
            op2 = int(input('Digite o número correspondente à opção desejada: '))
            print()
            
            if op2 < 1 or op2 > 4:
                print('='*70)
                print()
                print('OPÇÃO INDISPONÍVEL')
                print()

            elif op2 == 1:
                while True:
                    print('='*70)
                    print()
                    print('CADASTRO DE CLIENTES')
                    print()
                    print('OPÇÕES:')
                    print()
                    print('(1) Sócio')
                    print('(2) Não-sócio')
                    print()
                    
                    while True:
                        op3 = int(input('Digite o número correspondente à opção desejada: '))
                        if op3 != 1 and op3 != 2:
                            print('OPÇÃO INDISPONÍVEL')
                        else:
                            break
                        
                    print()
                    print('-'*70)
                    print()
                    
                    if op3 == 1:
                        print('SÓCIO')
                        tipo = 'Sócio'
                    else:
                        print('NÃO-SÓCIO')
                        tipo = 'Não-sócio'
                    
                    print()
                    
                    while True:
                        cpf = input('Digite o CPF do cliente (apenas números): ')
                        if cpf in clientes:
                            print('JÁ HÁ UM CLIENTE COM ESTE CPF')
                            print()
                        elif len(cpf) != 11:
                            print('CPF inválido')
                            print()
                        else:
                            break
                    
                    nome = input('Digite o nome completo do cliente: ')
 
                    while True:
                        telefone = input('Digite o número de telefone do cliente (com DDD e apenas números): ')
                        if len(telefone) != 11:
                            print('NÚMERO DE TELEFONE INVÁLIDO')
                            print()
                        else:
                            break
                    
                    print()
                    print(f'TIPO DE CLIENTE: {tipo}')
                    print(f'NOME: {nome}')
                    print(f'CPF: {cpf}')
                    print(f'TELEFONE: {telefone}')
                    
                    while True:
                        print()
                        cadastrar = input('Deseja cadastrar este cliente? Digite "S" ou "N": ').upper()
                        if cadastrar != 'S' and cadastrar != 'N':
                            print('AS OPÇÕES POSSÍVEIS SÃO "S" E "N"')    
                        else:
                            break
                    
                    if cadastrar == 'S' and op3 == 1:
                        cliente = Socio(cpf, nome, telefone)
                        clientes[cpf] = cliente
                        print()
                        print(f'CLIENTE DE CPF {cpf} CADASTRADO')
                        print()
                        print('='*70)
                        
                    elif cadastrar == 'S' and op3 == 2:
                        cliente = Nao_socio(cpf, nome, telefone)
                        clientes[cpf] = cliente
                        print()
                        print(f'CLIENTE DE CPF {cpf} CADASTRADO')
                        print()
                        print('='*70)

                    print()
                    
                    while True:
                        novo_cliente = input('Deseja cadastrar um novo cliente? Digite "S" ou "N": ').upper()
                        if cadastrar != 'S' and cadastrar != 'N':
                            print('AS OPÇÕES POSSÍVEIS SÃO "S" E "N"')    
                        else:
                            break
                    
                    print()
                    
                    if novo_cliente == 'N':
                        break
                    
            elif op2 == 2:
                print('='*70)
                print()
                print('EXCLUSÃO DE CLIENTES:')
                print()
                
                while True:
                    cpf = input('Digite o CPF do cliente que deseja excluir (digite 0 para sair): ')
                    
                    if cpf in clientes:
                        while True:
                            print()
                            excluir = input(f'Deseja mesmo excluir o cliente de CPF {cpf}? Digite "S" ou "N": ').upper()
                            if excluir != 'S' and excluir != 'N':
                                print('AS OPÇÕES POSSÍVEIS SÃO "S" E "N"')    
                            else:
                                print()
                                break
                            
                        if excluir == 'S':
                            del clientes[cpf]
                            print(f'CLIENTE DE CPF {cpf} EXCLUÍDO')
                            print()
                            print('='*70)
                            print()
                        
                    elif cpf == '0':
                        break
                    
                    else:
                        print('NÃO HÁ NENHUM CLIENTE CADASTRADO COM ESTE CPF')
                        print()

            elif op2 == 3:
                print('='*70)
                print()
                print('LISTA DE CLIENTES CADASTRADOS:')
                print()
                print('-'*70)
                print()
                
                for cpf in clientes:
                    cliente = clientes[cpf]
                    print('CPF:', cliente.get_cpf())
                    print('NOME:', cliente.get_nome())
                    print('TIPO:', cliente.get_tipo())
                    print('TELEFONE:', cliente.get_telefone())
                    print()
                    print('-'*70)
                    print()
                    
                print('OPÇÕES: ')
                print()
                print('(1) Alterar dados de um cliente')
                print('(2) Voltar ao menu anterior')
                print()
                
                while True:
                    op3 = int(input('Escolha uma opção: '))
                    if op3 != 1 and op3 != 2:
                        print('As opções são "1" e "2"')
                    else:
                        break
                
                print()
                
                if op3 == 1:
                    print('='*70)
                    print()
                    print('ALTERAÇÃO DE DADOS DE UM CLIENTE:')
                    
                    while True:
                        print()
                        cpf = input('Digite o número CPF do cliente que você deseja alterar (digite 0 para sair): ')
                        
                        if cpf in clientes:
                            cliente = clientes[cpf]
                            
                            print()
                            print('OPÇÕES:')
                            print()
                            print('(1) CPF')
                            print('(2) NOME')
                            print('(3) TELEFONE')
                            print('(4) VOLTAR AO MENU ANTERIOR')
                            print()
                          
                            while True:
                                op4 = int(input('Escolha uma opção: '))
                                if op4 < 1 or op4 > 4:
                                    print('OPÇÃO INDISPONÍVEL')
                                    print()
                                else:
                                    break
                                    
                            if op4 == 1:
                                print()
                                cpf_antigo = cpf
                                while True:
                                    cpf = input('Digite o CPF do cliente (apenas números): ')
                                    if cpf in clientes:
                                        print('JÁ HÁ UM CLIENTE COM ESTE CPF')
                                        print()
                                    elif len(cpf) != 11:
                                        print('CPF inválido')
                                        print()
                                    else:
                                        break
                                cliente.set_cpf(cpf)
                                clientes[cpf] = cliente
                                del clientes[cpf_antigo]
                                print()
                                print('CPF ALTERADO COM SUCESSO')
                                print()
                                print('-'*70)
                                
                            elif op4 == 2:
                                print()
                                nome = input('Digite o nome do cliente: ')
                                cliente.set_nome(nome)
                                print()
                                print('NOME ALTERADO COM SUCESSO')
                                print()
                                print('-'*70)
                            
                            elif op4 == 3:
                                while True:
                                    print()
                                    telefone = input('Digite o telefone do cliente (com DDD e apenas números: ')
                                    if len(telefone) != 11:
                                        print('NÚMERO DE TELEFONE INVÁLIDO')
                                    else:
                                        break
                                cliente.set_telefone(telefone)
                                print()
                                print('TELEFONE ALTERADO COM SUCESSO')
                                print()
                                print('-'*70)
                                
                            elif op4 == 4:
                                print()
                                break
                                
                        elif cpf == '0':
                            print()
                            break
                            
                        else:
                            print('NÃO HÁ NENHUM CLIENTE CADASTRADO COM ESTE CPF')
                            
            else:
                break

    elif op1 == 3:
        while True:
            print('='*70)
            print()
            print('GERENCIAMENTO DE RESERVAS')
            print()
            print('OPÇÕES:')
            print()
            print('(1) Cadastrar nova reserva')
            print('(2) Excluir uma reserva')
            print('(3) Consultar reservas')
            print('(4) Voltar ao menu inicial')
            print()
            op2 = int(input('Digite o número correspondente à opção desejada: '))
            print()
            
            if op2 < 1 or op2 > 4:
                print('='*70)
                print()
                print('OPÇÃO INDISPONÍVEL')
                print()
            
            elif op2 == 1:
                print('='*70)
                print()
                print('CADASTRO DE RESERVAS:')
                print()
                while True:
                    continuar = 1
                    
                    while True:
                        n_reserva = int(input('Digite o número da reserva (não pode ser 0): '))
                        if n_reserva == 0:
                            print('O NÚMERO DA RESERVA NÃO PODE SER 0')
                            print()
                        if n_reserva in reservas:
                            print('JÁ HÁ UMA RESERVA COM ESTE NÚMERO')
                            print()
                        else:
                            break
                    
                    while True:
                        cpf = input('Digite o CPF do cliente titular da reserva (apenas números/digite "0" para sair): ')
                        if cpf == '0':
                            continuar = 0
                            break
                        elif cpf not in clientes:
                            print('NÃO HÁ NENHUM CLIENTE CADASTRADO COM ESTE CPF')
                            print()
                        else:
                            break
                    
                    if continuar == 1:
                        while True:
                            n_identificacao = int(input('Digite o número de identificação da quadra a ser reservada (digite "0" para sair): '))
                            if n_identificacao == 0:
                                continuar = 0
                                break
                            if n_identificacao not in quadras:
                                print('NÃO HÁ NENHUMA QUADRA CADASTRADA COM ESTE NÚMERO DE IDENTIFICAÇÃO')
                                print()
                            else:
                                break
                    
                    if continuar == 1:

                        ano = int(input('Digite o ano em que será feita a reserva: '))
                            
                        while True:
                            mes = int(input('Digite o mês que será feita a reserva: '))
                            if mes < 1 or mes > 12:
                                print('O ano deve estar entre 1 e 12')
                                print()
                            else:
                                break

                        while True:
                            dia = int(input('Digite o dia em que será feita a reserva: '))
                            if ano % 4 == 0 and mes == 2 and dia > 29:
                                print('O dia deve ser no máximo 29')
                                print()
                            elif mes == 2 and dia > 28:
                                print('O dia deve ser no máximo 28')
                                print()
                            elif mes <= 7 and mes % 2 == 1 and dia > 31:
                                print('O dia deve ser no máximo 31')
                                print()
                            elif mes <= 7 and mes % 2 == 0 and dia > 30:
                                print('O dia deve ser no máximo 30')
                                print()
                            elif mes > 7 and mes % 2 == 0 and dia > 31:
                                print('O dia deve ser no máximo 31')
                                print()
                            elif mes > 7 and mes % 2 == 1 and dia > 30:
                                print('O dia deve ser no máximo 30')
                                print()
                            else:
                                break
                            
                        while True:
                            continuar = 1
                            hora = int(input('Digite o horário da reserva (entre 8h e 23h): '))
                            if hora < 8 or hora > 23:
                                print('O horário deve estar entre 8h e 23h')
                                print()
                                continuar = 0
                            else:
                                for n_reserva in reservas:
                                    reserva = reservas[n_reserva]
                                    if reserva.get_n_identificacao() == n_identificacao:
                                        if reserva.get_ano() == ano and reserva.get_mes() == mes and reserva.get_dia() == dia:
                                            if reserva.get_hora() <= hora < (reserva.get_hora() + reserva.get_duracao()):
                                                print(f'No momento em que você quer fazer a reserva já há uma reserva que se encerra às {reserva.get_hora() + reserva.get_duracao()}h')
                                                print()
                                                continuar = 0
                                                break
                            if continuar == 1:
                                break
                            
                        while True:
                            continuar = 1
                            duracao = int(input('Digite a duração em horas da reserva (não pode passar das 23h): '))
                            if duracao < 1 or duracao + hora > 23:
                                print('A DURAÇÃO MÍNIMA É 1H E A RESERVA NÃO PODE PASSAR DAS 23H')
                                print()
                            else:
                                for n_reserva in reservas:
                                    reserva = reservas[n_reserva]
                                    if reserva.get_n_identificacao() == n_identificacao:
                                        if reserva.get_ano() == ano and reserva.get_mes() == mes and reserva.get_dia() == dia:
                                            if hora < reserva.get_hora() and hora + duracao > reserva.get_hora():
                                                print(f'A sua reserva está invadindo o horário de uma reserva que começa às {reserva.get_hora()}h')
                                                print()
                                                continuar = 0
                                                break
                            if continuar == 1:
                                break

                        print()
                        print(f'NÚMERO DA RESERVA: {n_reserva}')
                        print(f'CPF: {cpf}')
                        print(f'QUADRA: {n_identificacao}')
                        print(f'DATA: {dia}/{mes}/{ano}')
                        print(f'HORA: {hora}h')
                        print(f'DURAÇÃO: {duracao}h')
                        
                        while True:
                            print()
                            cadastrar = input('Deseja cadastrar esta reserva? Digite "S" ou "N": ').upper()
                            if cadastrar != 'S' and cadastrar != 'N':
                                print('AS OPÇÕES POSSÍVEIS SÃO "S" E "N"')    
                            else:
                                break
                        
                        if cadastrar == 'S':
                            cliente = clientes[cpf]
                            quadra = quadras[n_identificacao]
                            reserva = Reserva(n_reserva, cpf, cliente, n_identificacao, quadra, ano, mes, dia, hora, duracao)
                            reservas[n_reserva] = reserva
                            print()
                            print(f'RESERVA {n_reserva} CADASTRADA')
                            print(f'VALOR: {reserva.get_valor()} Reais')
                            print()
                            print('='*70)
                        
                        print()
                        
                        while True:
                            nova_reserva = input('Deseja cadastrar uma nova reserva? Digite "S" ou "N": ').upper()
                            if cadastrar != 'S' and cadastrar != 'N':
                                print('AS OPÇÕES POSSÍVEIS SÃO "S" E "N"')    
                            else:
                                break
                    
                    print()
                    
                    if continuar == 0:
                        break
                    elif nova_reserva == 'N':
                        break
                    
            elif op2 == 2:
                print('='*70)
                print()
                print('EXCLUSÃO DE RESERVAS:')
                print()
                
                while True:
                    n_reserva = int(input('Digite o número da reserva que deseja excluir (digite 0 para sair): '))
                    
                    if n_reserva in reservas:
                        while True:
                            print()
                            excluir = input(f'Deseja mesmo excluir a reserva {n_reserva}? Digite "S" ou "N": ').upper()
                            if excluir != 'S' and excluir != 'N':
                                print('AS OPÇÕES POSSÍVEIS SÃO "S" E "N"')    
                            else:
                                print()
                                break
                            
                        if excluir == 'S':
                            del reservas[n_reserva]
                            print(f'RESERVA {n_reserva} EXCLUÍDA')
                            print()
                            print('='*70)
                            print()
                        
                    elif n_reserva == 0:
                        break
                    
                    else:
                        print('NÃO HÁ NENHUMA RESERVA CADASTRADA COM ESTE NÚMERO')
                        print()

            elif op2 == 3:
                print('='*70)
                print()
                print('LISTA DE RESERVAS CADASTRADAS:')
                print()
                print('-'*70)
                print()
                
                for n_reserva in reservas:
                    reserva = reservas[n_reserva]
                    print('RESERVA NÚMERO:', reserva.get_n_reserva())
                    print()
                    print('CPF:', reserva.get_cpf())
                    print('QUADRA:', reserva.get_n_identificacao())
                    print(f'DATA: {reserva.get_dia()}/{reserva.get_mes()}/{reserva.get_dia()}')
                    print(f'HORA: {reserva.get_hora()}h')
                    print(f'DURAÇÃO: {reserva.get_duracao()}h')
                    print('VALOR:', reserva.get_valor(), 'Reais')
                    print()
                    print('-'*70)
                    print()
                            
                op3 = input('Digite qualquer coisa para sair: ')
                print()
                
            else:
                break