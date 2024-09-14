'''
#exercicio 1

s = input('Qual o seu sexo (M ou F)? ').upper()
while s != 'M' and s != 'F':
    s = input('Digite um valor correto (M ou F)').upper()

#exercicio 2

from random import randrange
n = randrange(10)
tentativas = 1
palpite = int(input('Digite um número de 0 a 10: '))
while palpite != n:
    palpite = int(input('Tente outro número: '))
    tentativas += 1
print(f'Você acertou em {tentativas} tentativas!')

#exercicio 3
continuar = 'S'
while continuar == 'S':
    salario = float(input('Valor do salário que sofrerá o desconto: '))
    if 0.11 * salario >= 320:
        desconto = (320 / salario) * 100
        print(f'O desconto será de R$320, representando {desconto}% do salário')
    else:
        desconto = 0.11 * salario
        print(f'O desconto será de R${desconto}, representando 11% do salário')
    continuar = input('Deseja calcular mais um desconto (S/N)? ').upper()

#exercicio 4

a = 1
N = int(input('Digite um número: '))
while a < 10001:
    if a % N == 2:
        print(a)
    a += 1

#exercicio 5

a = 1
N = int(input('Digite um número: '))
while a < 11:
    b = N * a
    print(f'{N} x {a} = {b}')
    a += 1

#exercicio 6

X = int(input('Digite um número: '))
while X != 0:
    a = 1
    while a <= X:
        print (a, end=' ')
        a += 1
    print('\n')
    X = int(input('Digite um número: '))

#exercicio 7

tipo = a = g = d = 0
while tipo != '4':
    tipo = input('Digite qual combustível foi abastecido: \n(1) Álcool\n(2) Gasolina\n(3) Diesel\n(4) Encerrar programa\n')
    if tipo == '1':
        a += 1
    elif tipo == '2':
        g += 1
    elif tipo == '3':
        d += 1
print(f'MUITO OBRIGADO\nÁlcool: {a}\nGasolina: {g}\nDiesel: {d}')

#exercicio 8

while True:
    M, N = input('Digite dois números separados por um espaço: ').split()
    M = int(M)
    N = int(N)
    soma = 0
    if M == 0 or N == 0:
        break
    elif M > N:
        a = N
        b = M
    elif N > M:
        a = M
        b = N
    while a <= b:
        soma += a
        print(a, end=' ')
        a += 1
    if N == M:
        print(N, end=' ')
    print(f'Sum={soma}')
'''