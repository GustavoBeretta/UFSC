from lista_automoveis_disponiveis import Lista_automoveis_disponiveis
from lista_automoveis import Lista_automoveis
from lista_clientes import Lista_clientes
from lista_reservas import Lista_reservas
from carro import Carro
from moto import Moto
from reserva import Reserva
from cliente import Cliente

#senha fixa do sistema
senha = '123'

#tela de login do sistema
while True:
    print('='*70)
    print(' '*26 + 'LOGIN DO SISTEMA')
    print()

    login = input('DIGITE A SENHA: ')
    print()
    
    #verificação da senha
    if login != senha:
        print('='*70)
        print()
        print('SENHA INCORRETA')
        print()
    
    else:
        
        #criação dos dicionários de armazenamento em suas respectivas classes
        lista_automoveis_disponiveis = Lista_automoveis_disponiveis()
        lista_automoveis = Lista_automoveis()
        lista_clientes = Lista_clientes()
        lista_reservas = Lista_reservas()
        
        #menu principal do sistema
        while True:
            print('='*70)
            print(' '*28 + 'MENU DO SISTEMA')
            print()
            print('OPERAÇÕES: ')
            print()
            print('(1) Gerenciar automóveis')
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
            
            #menu de gerenciamento dos automóveis
            elif op1 == 1:
                while True:
                    print('='*70)
                    print()
                    print('GERENCIAMENTO DE AUTOMÓVEIS')
                    print()
                    print('OPÇÕES:')
                    print()
                    print('(1) Cadastrar novo automóvel')
                    print('(2) Excluir um automóvel disponível')
                    print('(3) Consultar automóveis disponíveis')
                    print('(4) Voltar ao menu inicial')
                    print()
                    op2 = int(input('Digite o número correspondente à opção desejada: '))
                    print()
                
                    if op2 < 1 or op2 > 4:
                        print('='*70)
                        print()
                        print('OPÇÃO INDISPONÍVEL')
                        print()
                    
                    #sequência de cadastro de um novo automóvel
                    elif op2 == 1:
                        print('='*70)
                        print()
                        print('CADASTRO DE AUTOMÓVEIS:')
                        print()
                        while True:
                            
                            while True:
                                n_identificacao = int(input('Digite um número de identificação para o automóvel (não pode ser 0): '))
                                if n_identificacao in lista_automoveis.get_lista_automoveis():
                                    print('JÁ HÁ UM AUTOMÓVEL COM ESTE NÚMERO DE IDENTIFICAÇÃO')
                                    print()
                                elif n_identificacao == 0:
                                    print('O NÚMERO DE IDENTIFICAÇÃO NÃO PODE SER 0')
                                    print()
                                else:
                                    break
                            
                            while True:
                                print()
                                tipo = int(input('Digite o tipo de automóvel ("1" para carro ou "2" para moto): '))
                                if tipo != 1 and tipo != 2:
                                    print('OPÇÃO INDISPONÍVEL')
                                else:
                                    break
                            
                            modelo = input('Digite a descrição do automóvel (marca, modelo, ano e cor): ')
                            
                            while True:
                                valor_diaria = float(input('Digite o valor em Reais da diária da reserva do automóvel: '))
                                if valor_diaria <= 0:
                                    print('O VALOR DEVE SER POSITIVO')
                                    print()
                                else:
                                    break
                            
                            #confirmação dos dados fornecidos
                            print()
                            print(f'NÚMERO DE IDENTIFICAÇÃO: {n_identificacao}')
                            if tipo == 1:
                                print('TIPO: Carro')
                            elif tipo == 2:
                                print('TIPO: Moto')                            
                            print(f'DESCRIÇÃO: {modelo}')
                            print(f'VALOR DA DIÁRIA: {valor_diaria} Reais')
                            
                            while True:
                                print()
                                cadastrar = input('Deseja cadastrar este automóvel? Digite "S" ou "N": ').upper()
                                if cadastrar != 'S' and cadastrar != 'N':
                                    print('AS OPÇÕES POSSÍVEIS SÃO "S" E "N"')    
                                else:
                                    break
                            
                            #cadastro do novo automóvel
                            if cadastrar == 'S':
                                if tipo == 1:
                                    automovel = Carro(n_identificacao, modelo, valor_diaria)
                                elif tipo == 2:
                                    automovel = Moto(n_identificacao, modelo, valor_diaria)
                                lista_automoveis.get_lista_automoveis()[n_identificacao] = automovel
                                lista_automoveis_disponiveis.get_lista_automoveis_disponiveis()[n_identificacao] = automovel
                                print()
                                print(f'AUTOMÓVEL {n_identificacao} CADASTRADO')
                                print()
                                print('='*70)
                            
                            while True:
                                print()
                                novo_automovel = input('Deseja cadastrar um novo automóvel? Digite "S" ou "N": ').upper()
                                if novo_automovel != 'S' and novo_automovel != 'N':
                                    print('AS OPÇÕES POSSÍVEIS SÃO "S" E "N"')    
                                else:
                                    break
                            
                            print()
                            
                            if novo_automovel == 'N':
                                break
                            
                    #menu de exclusão de automóveis não envolvidos com reservas no momento
                    elif op2 == 2:
                        print('='*70)
                        print()
                        print('EXCLUSÃO DE AUTOMÓVEIS DISPONÍVEIS:')
                        print()
                        
                        while True:
                            n_identificacao = int(input('Digite o número de identificação do automóvel que deseja excluir (digite 0 para sair): '))
                            
                            if n_identificacao in lista_automoveis_disponiveis.get_lista_automoveis_disponiveis():
                                while True:
                                    print()
                                    excluir = input(f'Deseja mesmo excluir o automóvel {n_identificacao}? Digite "S" ou "N": ').upper()
                                    if excluir != 'S' and excluir != 'N':
                                        print('AS OPÇÕES POSSÍVEIS SÃO "S" E "N"')    
                                    else:
                                        print()
                                        break
                                    
                                if excluir == 'S':
                                    del lista_automoveis_disponiveis.get_lista_automoveis_disponiveis()[n_identificacao]
                                    del lista_automoveis.get_lista_automoveis()[n_identificacao]
                                    print(f'AUTOMÓVEL {n_identificacao} EXCLUÍDO')
                                    print()
                                    print('='*70)
                                    print()
                                
                            elif n_identificacao == 0:
                                break
                            
                            else:
                                print('O AUTOMÓVEL CADASTRADO COM ESTE NÚMERO DE IDENTIFICAÇÃO NÃO ESTÁ DISPONÍVEL OU NÃO EXISTE')
                                print()
                    
                    #menu de consulta dos automóveis cadastrados disponíveis para aluguel
                    elif op2 == 3:
                        print('='*70)
                        print()
                        print('LISTA DE AUTOMÓVEIS DISPONÍVEIS:')
                        print()
                        print('-'*70)
                        print()
                        
                        for n_identificacao in lista_automoveis_disponiveis.get_lista_automoveis_disponiveis():
                            automovel = lista_automoveis_disponiveis.get_lista_automoveis_disponiveis()[n_identificacao]
                            print('AUTOMÓVEL NÚMERO:', automovel.get_n_identificacao())
                            print()
                            print('TIPO:', automovel.get_tipo())
                            print('DESCRIÇÃO:', automovel.get_modelo())
                            print('VALOR DA DIÁRIA:', automovel.get_valor_diaria(), 'Reais')
                            print()
                            print('-'*70)
                            print()
                            
                        print('OPÇÕES: ')
                        print()
                        print('(1) Alterar dados de um automóvel')
                        print('(2) Voltar ao menu anterior')
                        print()
                        
                        while True:
                            op3 = int(input('Escolha uma opção: '))
                            if op3 != 1 and op3 != 2:
                                print('As opções são "1" e "2"')
                            else:
                                break
                        
                        print()
                        
                        #menu de alteração de dados de um automóvel disponível
                        if op3 == 1:
                            print('='*70)
                            print()
                            print('ALTERAÇÃO DE DADOS DE UM AUTOMÓVEL:')
                            
                            while True:
                                print()
                                n_identificacao = int(input('Digite o número de identificação do automóvel que você deseja alterar (digite 0 para sair): '))
                                
                                if n_identificacao in lista_automoveis_disponiveis.get_lista_automoveis_disponiveis():
                                    automovel = lista_automoveis_disponiveis.get_lista_automoveis_disponiveis()[n_identificacao]
                                    
                                    print()
                                    print('OPÇÕES:')
                                    print()
                                    print('(1) NÚMERO DE IDENTIFICAÇÃO')
                                    print('(2) DESCRIÇÃO')
                                    print('(3) VALOR DA DIÁRIA')
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
                                        n_antigo = n_identificacao #armazenando o número de identificação antigo para excluir o objeto no dicionário
                                        while True:
                                            n_identificacao = int(input('Digite o novo número de identificação do automóvel (não pode ser 0): '))
                                            if n_identificacao in lista_automoveis.get_lista_automoveis():
                                                print('JÁ HÁ UM AUTOMÓVEL COM ESTE NÚMERO DE IDENTIFICAÇÃO')
                                                print()
                                            elif n_identificacao == 0:
                                                print('O NÚMERO DE IDENTIFICAÇÃO NÃO PODE SER 0')
                                                print()
                                            else:
                                                break
                                        automovel.set_n_identificacao(n_identificacao) #muda o número de identificação do objeto automovel
                                        lista_automoveis.get_lista_automoveis()[n_identificacao] = automovel #dicionário de armazenamento recebe o objeto com o número de identificação correto
                                        lista_automoveis_disponiveis.get_lista_automoveis_disponiveis()[n_identificacao] = automovel #dicionário de armazenamento recebe o objeto com o número de identificação correto
                                        del lista_automoveis.get_lista_automoveis()[n_antigo] #objeto com número de identificação incorreto é deletado do dicionário de armazenamento
                                        del lista_automoveis_disponiveis.get_lista_automoveis_disponiveis()[n_antigo] #objeto com número de identificação incorreto é deletado do dicionário de armazenamento
                                        print()
                                        print('NÚMERO DE IDENTIFICAÇÃO ALTERADO COM SUCESSO')
                                        print()
                                        print('-'*70)
                                        
                                    elif op4 == 2:
                                        print()
                                        modelo = input('Digite a nova descrição do automóvel (marca, modelo, ano e cor): ')
                                        automovel.set_modelo(modelo)
                                        print()
                                        print('DESCRIÇÃO ALTERADA COM SUCESSO')
                                        print()
                                        print('-'*70)
                                    
                                    elif op4 == 3:
                                        while True:
                                            print()
                                            valor_diaria = float(input('Digite o valor em Reais da diária da reserva do veículo: '))
                                            if valor_diaria <= 0:
                                                print('O VALOR DEVE SER POSITIVO')
                                            else:
                                                break
                                        automovel.set_valor_diaria(valor_diaria)
                                        print()
                                        print('VALOR DA DIÁRIA DA RESERVA ALTERADO COM SUCESSO')
                                        print()
                                        print('-'*70)
                                    
                                    elif op4 == 4:
                                        print()
                                        break
                                        
                                elif n_identificacao == 0:
                                    print()
                                    break
                                    
                                else:
                                    print('O AUTOMÓVEL CADASTRADO COM ESTE NÚMERO DE IDENTIFICAÇÃO NÃO ESTÁ DISPONÍVEL OU NÃO EXISTE')
                                    
                    else:
                        break
            
            #menu de gerenciamento de clientes
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
                    
                    #sequência de cadastro de novo cliente
                    elif op2 == 1:
                        while True:
                            print('='*70)
                            print()
                            print('CADASTRO DE CLIENTES')
                            print()

                            while True:
                                cpf = input('Digite o CPF do cliente (apenas números): ')
                                if cpf in lista_clientes.get_lista_clientes():
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
                            
                            #confirmação dos dados fornecidos
                            print()
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
                            
                            #cadastro do novo cliente
                            if cadastrar == 'S':
                                cliente = Cliente(cpf, nome, telefone)
                                lista_clientes.get_lista_clientes()[cpf] = cliente
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
                    
                    #menu de exclusão de um cliente já cadastrado
                    elif op2 == 2:
                        print('='*70)
                        print()
                        print('EXCLUSÃO DE CLIENTES:')
                        print()
                        
                        while True:
                            cpf = input('Digite o CPF do cliente que deseja excluir (digite 0 para sair): ')
                            
                            if cpf in lista_clientes.get_lista_clientes():
                                while True:
                                    print()
                                    excluir = input(f'Deseja mesmo excluir o cliente de CPF {cpf}? Digite "S" ou "N": ').upper()
                                    if excluir != 'S' and excluir != 'N':
                                        print('AS OPÇÕES POSSÍVEIS SÃO "S" E "N"')    
                                    else:
                                        print()
                                        break
                                    
                                if excluir == 'S':
                                    del lista_clientes.get_lista_clientes()[cpf]
                                    print(f'CLIENTE DE CPF {cpf} EXCLUÍDO')
                                    print()
                                    print('='*70)
                                    print()
                                
                            elif cpf == '0':
                                break
                            
                            else:
                                print('NÃO HÁ NENHUM CLIENTE CADASTRADO COM ESTE CPF')
                                print()
                    #consulta dos cllientes cadastrados
                    elif op2 == 3:
                        print('='*70)
                        print()
                        print('LISTA DE CLIENTES CADASTRADOS:')
                        print()
                        print('-'*70)
                        print()
                        
                        for cpf in lista_clientes.get_lista_clientes():
                            cliente = lista_clientes.get_lista_clientes()[cpf]
                            print('CPF:', cliente.get_cpf())
                            print('NOME:', cliente.get_nome())
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
                        
                        #menu de alteração de dados de um cliente já cadastrado
                        if op3 == 1:
                            print('='*70)
                            print()
                            print('ALTERAÇÃO DE DADOS DE UM CLIENTE:')
                            
                            while True:
                                print()
                                cpf = input('Digite o número CPF do cliente que você deseja alterar (digite 0 para sair): ')
                                
                                if cpf in lista_clientes.get_lista_clientes():
                                    cliente = lista_clientes.get_lista_clientes()[cpf]
                                    
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
                                            if cpf in lista_clientes.get_lista_clientes():
                                                print('JÁ HÁ UM CLIENTE COM ESTE CPF')
                                                print()
                                            elif len(cpf) != 11:
                                                print('CPF inválido')
                                                print()
                                            else:
                                                break
                                        cliente.set_cpf(cpf)
                                        lista_clientes.get_lista_clientes()[cpf] = cliente
                                        del lista_clientes.get_lista_clientes()[cpf_antigo]
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
            
            #menu de gerenciamento de reservas
            elif op1 == 3:
                while True:
                    print('='*70)
                    print()
                    print('GERENCIAMENTO DE RESERVAS')
                    print()
                    print('OPÇÕES:')
                    print()
                    print('(1) Cadastrar nova reserva')
                    print('(2) Finalizar uma reserva')
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
                    
                    #sequência de cadastro de nova reserva
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
                                if n_reserva in lista_reservas.get_lista_reservas():
                                    print('JÁ HÁ UMA RESERVA COM ESTE NÚMERO')
                                    print()
                                else:
                                    break
                            
                            while True:
                                cpf = input('Digite o CPF do cliente titular da reserva (apenas números/digite "0" para sair): ')
                                if cpf == '0':
                                    continuar = 0
                                    break
                                elif cpf not in lista_clientes.get_lista_clientes():
                                    print('NÃO HÁ NENHUM CLIENTE CADASTRADO COM ESTE CPF')
                                    print()
                                else:
                                    break
                            
                            if continuar == 1:
                                while True:
                                    n_identificacao = int(input('Digite o número de identificação do automóvel a ser reservado (digite "0" para sair): '))
                                    if n_identificacao == 0:
                                        continuar = 0
                                        break
                                    if n_identificacao not in lista_automoveis_disponiveis.get_lista_automoveis_disponiveis():
                                        print('O AUTOMÓVEL CADASTRADO COM ESSE NÚMERO DE IDENTIFICAÇÃO NÃO ESTÁ DISPONÍVEL OU NÃO EXISTE')
                                        print()
                                    else:
                                        break
                            
                            if continuar == 1:     
                                
                                #confirmação dos dados fornecidos
                                print()
                                print(f'NÚMERO DA RESERVA: {n_reserva}')
                                print(f'CPF: {cpf}')
                                print(f'AUTOMÓVEL: {n_identificacao}')

                                while True:
                                    print()
                                    cadastrar = input('Deseja cadastrar esta reserva? Digite "S" ou "N": ').upper()
                                    if cadastrar != 'S' and cadastrar != 'N':
                                        print('AS OPÇÕES POSSÍVEIS SÃO "S" E "N"')    
                                    else:
                                        break
                                
                                #cadastro de nova reserva
                                if cadastrar == 'S':
                                    cliente = lista_clientes.get_lista_clientes()[cpf] #pegando os dados do cliente do dicionário de armazenamento
                                    automovel = lista_automoveis_disponiveis.get_lista_automoveis_disponiveis()[n_identificacao] #pegando os dados do automóvel do dicionário de armazenamento
                                    reserva = Reserva(n_reserva, cpf, cliente, n_identificacao, automovel)
                                    lista_reservas.get_lista_reservas()[n_reserva] = reserva
                                    del lista_automoveis_disponiveis.get_lista_automoveis_disponiveis()[n_identificacao] #deletanto o automóvel da lista de automóveis disponíveis para aluguel
                                    print()
                                    print(f'RESERVA {n_reserva} CADASTRADA')
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
                    
                    #menu de finalização de reservas
                    elif op2 == 2:
                        print('='*70)
                        print()
                        print('FINALIZAÇÃO DE RESERVAS:')
                        print()
                        
                        while True:
                            n_reserva = int(input('Digite o número da reserva que deseja finalizar (digite 0 para sair): '))
                            
                            if n_reserva in lista_reservas.get_lista_reservas():
                                while True:
                                    print()
                                    finalizar = input(f'Deseja mesmo finalizar a reserva {n_reserva}? Digite "S" ou "N": ').upper()
                                    if finalizar != 'S' and finalizar != 'N':
                                        print('AS OPÇÕES POSSÍVEIS SÃO "S" E "N"')    
                                    else:
                                        print()
                                        break
                                
                                if finalizar == 'S':
                                    dias = int(input('Duração (em dias) da reserva: '))
                                    reserva = lista_reservas.get_lista_reservas()[n_reserva] #pegando a reserva a ser finalizada do dicionário de armazenamento
                                    n_identificacao = reserva.get_n_identificacao() #pegando o número de identificação do automóvel reservado
                                    automovel = lista_automoveis.get_lista_automoveis()[n_identificacao] #pegando o automóvel reservado para chamar o método que mostra o valor da diária
                                    valor_diaria = automovel.get_valor_diaria()
                                    valor_total = valor_diaria * dias
                                    print()
                                    print(f'VALOR TOTAL DA RESERVA: {valor_total} Reais')
                                    del lista_reservas.get_lista_reservas()[n_reserva]
                                    lista_automoveis_disponiveis.get_lista_automoveis_disponiveis()[n_identificacao] = automovel #adicionando o automóvel na lista de automóveis disponíveis para aluguel
                                    print(f'RESERVA {n_reserva} FINALIZADA')
                                    print()
                                    print('='*70)
                                    print()
                                
                            elif n_reserva == 0:
                                break
                            
                            else:
                                print('NÃO HÁ NENHUMA RESERVA CADASTRADA COM ESTE NÚMERO')
                                print()
                                
                    #consulta das reservas cadastradas
                    elif op2 == 3:
                        print('='*70)
                        print()
                        print('LISTA DE RESERVAS CADASTRADAS:')
                        print()
                        print('-'*70)
                        print()
                        
                        for n_reserva in lista_reservas.get_lista_reservas():
                            reserva = lista_reservas.get_lista_reservas()[n_reserva]
                            n_identificacao = reserva.get_n_identificacao()
                            automovel = lista_automoveis.get_lista_automoveis()[n_identificacao]
                            print('RESERVA NÚMERO:', reserva.get_n_reserva())
                            print()
                            print('CPF:', reserva.get_cpf())
                            print('AUTOMÓVEL:', automovel.get_n_identificacao())
                            print('MODELO:', automovel.get_modelo())
                            print('VALOR DA DIÁRIA:', automovel.get_valor_diaria())
                            print()
                            print('-'*70)
                            print()
                                    
                        op3 = input('Digite qualquer coisa para sair: ')
                        print()
                        
                    else:
                        break