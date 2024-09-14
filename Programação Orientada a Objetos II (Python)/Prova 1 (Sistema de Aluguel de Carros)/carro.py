from automovel import Automovel

#classe Carro que é uma herança da classe Automovel
class Carro(Automovel):
    def __init__(self, n_identificacao, modelo, valor_diaria):
        super().__init__(n_identificacao, modelo, valor_diaria)
        self.tipo = 'Carro'
    
    def get_tipo(self):
        return self.tipo