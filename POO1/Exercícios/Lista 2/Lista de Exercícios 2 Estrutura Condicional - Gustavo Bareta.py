'''
#exercício 1

valor = float(input('Valor da casa (R$): '))
salario = float(input('Salário do comprador (R$): '))
tempo = int(input('Anos para a quitação da dívida: '))
prestacao = valor / (tempo * 12)
if (prestacao > (salario * 0.3)):
    print('A prestação corresponde a mais de 30% do seu salário, o empréstimo não pode ser efetuado')
else:
    print(f'Seu empréstimo foi aceito! A prestação será de R${prestacao} por mês.')

#exercício 2

valor_std = int(input('Valor do produto (R$): '))
forma_pag = input(' A) À vista (dinheiro ou cheque) - 10% de desconto\n B) 1x no cartão - 5% de desconto\n C) 2x no cartão - preço padrão\n D) 3x ou mais no cartão - 20% de juros\nForma de pagamento (digite: A, B, C ou D): ')
if forma_pag == 'A':
    novo_valor = valor_std * 0.9
    print(f'O valor a ser pago é de R${novo_valor}.')
elif forma_pag == 'B':
    novo_valor = valor_std * 0.95
    print(f'O valor a ser pago é de R${novo_valor}.')
elif forma_pag == 'C':
    print(f'O valor a ser pago é de R${valor_std}.')
elif forma_pag == 'D':
    novo_valor = valor_std * 1.2
    print(f'O valor a ser pago é de R${novo_valor}.')
else:
    print('Escolha uma forma de pagamento válida.')

#exercício 3

peso = float(input('Seu peso (kg): '))
altura = float(input('Sua altura (m): '))
IMC = peso / altura**2
if IMC < 18.5:
    print('Cuidado, você está abaixo do peso ideal.')
elif 18.5 <= IMC < 25:
    print('Parabéns! Você está no peso ideal.')
elif 25 <= IMC < 30:
    print('Cuidado, você está com sobrepeso.')
elif 30 <= IMC < 40:
    print('Procure ajuda, você está com obesidade.')
else:
    print('Procure ajuda urgentemente! Você está com obesidade mórbida.')

#exercício 4
 
n1 = float(input('Nota 1: '))
n2 = float(input('Nota 2: '))
n3 = float(input('Nota 3: '))
m = (n1 + n2 + n3) / 3
print('Sua média é {:.2f}'.format(m))
if m < 5:
    print('Você está reprovado.')
elif 5 <= m < 7:
    print('Você está de recuperação.')
else:
    print('Parabéns! Você está aprovado.')

#exercício 1051

salario = float(input('Seu salário: '))
if salario <= 2000:
    print('Isento')
elif 2000 < salario <= 3000:
    IR = (salario - 2000) * 0.08
    print(f'R${IR}')
elif 3000 < salario <= 4500:
    IR = (salario - 3000) * 0.18 + 80
    print(f'R${IR}')
else:
    IR = (salario - 4500) * 0.28 + 350
    print(f'R${IR}')
'''