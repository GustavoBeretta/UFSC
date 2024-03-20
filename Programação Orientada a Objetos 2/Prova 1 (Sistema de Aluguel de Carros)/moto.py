from automovel import Automovel

#classe Moto que é uma herança da classe Automovel
class Moto(Automovel):
    def __init__(self, n_identificacao, modelo, valor_diaria):
        super().__init__(n_identificacao, modelo, valor_diaria)
        self.tipo = 'Moto'
        
    def get_tipo(self):
        return self.tipo