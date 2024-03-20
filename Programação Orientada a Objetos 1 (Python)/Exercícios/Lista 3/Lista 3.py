'''
#exercício 1

for i in range (2004,2097,4):
    print(i)
 
#exercício 2

for i in range (1,50,2):
    print(i)

#exercício 3

for i in range (5):
    nome = input('Nome do aluno: ')
    media = float(input('Média geral: '))
    mensalidade = float(input('Mensalidade: '))
    nome_aux = nome
    nota = media
    valor = mensalidade
    if media > nota:
        nome_aux = nome
        nota = media
        valor = mensalidade
print(nome_aux)
print(mensalidade)
print(mensalidade*0.7)

#exercício 4

p = 0
i = 0
for a in range (10):
    n = int(input('Escreva um número inteiro: '))
    if n % 2 == 0:
        p += 1
    else:
        i += 1
print(f'{p} números pares e {i} ímpares')

#exercício 5

resto_zero = 0
n = int(input('Escreva um número inteiro: '))
for a in range(1,n+1)
    if n % a == 0
        resto_zero += 1
if resto_zero == 2:
    print('É primo')
else:
    print('Não é primo')

#exercício 6

resto_zero = 0
n = int(input('Escreva um número inteiro: '))
for a in range(1,n+1):
    if n % a == 0:
        resto_zero += 1
if resto_zero == 2:
    print('É primo')
else:
    print('Não é primo')
    for a in range(1,n+1):
        if n % a == 0:
            print(a)

#exercício 7

soma = 0
n = int(input('Quantas pessoas serão perguntadas? '))
for a in range (n):
    idade = int(input('Qual a sua idade? '))
    soma += idade
media = soma / n
if media <= 25:
    print('A turma é jovem')
elif 25 < media <= 60:
    print('A turma é adulta')
else:
    print('A turma é idosa')

#exercício 9

n = int(input('De qual número você deseja ver a tabuada? '))
print (f'Tabuada de {n}')
for a in range (1,11):
    print(f'{n}x{a}={n*a}')
'''