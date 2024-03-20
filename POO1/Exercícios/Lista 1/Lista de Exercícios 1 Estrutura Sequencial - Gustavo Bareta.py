'''
#exercício 1

A = int(input('Valor inteiro A: '))
B = int(input('Valor inteiro B: '))
SOMA = A + B
print('SOMA =',SOMA)

#exercício 2

a = int(input('Valor inteiro A: '))
b = int(input('Valor inteiro B: '))
PROD = a * b
print('PROD =', PROD)

#exercício 3

A = float(input('Nota A (com uma casa decimal): '))
B = float(input('Nota B (com uma casa decimal): '))
media = (3.5*A + 7.5*B)/11
print('MEDIA = {:.5f}'.format(media))

#exercício 4

A = float(input('Nota A: '))
B = float(input('Nota B: '))
C = float(input('Nota C: '))
media = (A*2 + B*3 + C*5)/10
print('MEDIA = {:.1f}'.format(media))

#exercício 5

A = int(input('Valor inteiro A: '))
B = int(input('Valor inteiro B: '))
C = int(input('Valor inteiro C: '))
D = int(input('Valor inteiro D: '))
DIFERENCA = A*B-C*D
print('DIFERENCA =', DIFERENCA)

#exercício 6

n = input('Número do funcionário: ')
horas = int(input('Número de horas trabalhadas: '))
valor_hora = float(input('Valor da hora trabalhada: '))
salario = horas * valor_hora
print('NUMBER =', n)
print('SALARY = U$ {:.2f}'.format(salario))

#exercício 7

N = int(input('Pressão do pneu desejada: (Mín:1/Máx:40)'))
M = int(input('Pressão do pneu lida pela bomba: (Mín:1/Máx:40)'))
diferenca = N - M
print(diferenca)

#exercício 8

t = int(input('Quantidade de pessoas clicaram no 3° link: '))
p = t * 2**2
print(p)

#exercício 9

A = float(input('Valor A: '))
B = float(input('Valor B: '))
C = float(input('Valor C: '))
triangulo = (A*C)/2
circulo = (C**2)*3.14159
trapezio = ((A+B)*C)/2
quadrado = B**2
retangulo = A*B
print('TRIANGULO: {:.3f}'.format(triangulo))
print('CIRCULO: {:.3f}'.format(circulo))
print('TRAPEZIO: {:.3f}'.format(trapezio))
print('QUADRADO: {:.3f}'.format(quadrado))
print('RETANGULO: {:.3f}'.format(retangulo))

#exercício 10

idade = int(input('Sua idade em dias: '))
anos = idade // 365
meses = (idade % 365) // 30
dias = (idade % 365) % 30
print (anos,'ano(s)')
print (meses,'mes(es)')
print (dias,'dia(s)')

#exercício 11
x1, y1 = input('Coordenadas do ponto 1 (separe o valor de x do de y com um espaço): ').split()
x2, y2 = input('Coordenadas do ponto 2 (separe o valor de x do de y com um espaço): ').split()
x1 = float(x1)
y1 = float(y1)
x2 = float(x2)
y2 = float(y2)
d = (((x2-x1)**2) + ((y2-y1)**2))**0.5
print('{:.4f}'.format(d))

#exercício 12

N = int(input('Tempo do evento (em segundos): '))
h = N // 60 // 60
m = N // 60 % 60
s = N % 60
print(h,':',m,':',s)

#exercício 13

t = int(input('Tempo de viagem (em horas): '))
vm = int(input('Velociade média durante a viagem (em km/h): '))
d = t * vm
L = d / 12
print('{:.3f}'.format(L))

#exercício 14

X = int(input('Distância total percorrida (em km): '))
Y = int(input('Quantidade de litros de combustível gasta: '))
C = X / Y
print('{:.3f}km/l'.format(C))


#exercício 15

nome = input('Nome do vendedor: ')
salario_fixo = float(input('Salário do vendedor: '))
vendas = float(input('Valor das vendas efetuadas pelo vendedor: '))
salario = salario_fixo + 0.15 * vendas
print('TOTAL = R$ {:.2f}'.format(salario))
'''