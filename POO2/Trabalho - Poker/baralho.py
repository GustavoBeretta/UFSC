from random import randint

class Baralho():
    def __init__(self):
        self.baralho = []
        valores = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
        naipes = ('Espadas', 'Paus', 'Copas', 'Ouros')
        for valor in valores:
            for naipe in naipes:
                carta = valor + ' de ' + naipe
                self.baralho.append(carta)
        self.n_cartas = 52
    
    def pegar_carta_aleatoria(self):
        n_carta = randint(0,self.n_cartas - 1)
        carta = self.baralho[n_carta]
        del self.baralho[n_carta]
        self.n_cartas = self.n_cartas - 1
        return carta