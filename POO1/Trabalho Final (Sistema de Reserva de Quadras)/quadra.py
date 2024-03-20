class Quadra:
    def __init__(self, n_identificacao, esporte, valor_h, capacidade_max, cobertura):
        self.n_identificacao = n_identificacao
        self.esporte = esporte
        self.valor_h = valor_h
        self.capacidade_max = capacidade_max
        self.cobertura = cobertura
     
    def get_n_identificacao(self):
        return self.n_identificacao
    def get_esporte(self):
        return self.esporte
    def get_valor_h(self):
        return self.valor_h
    def get_capacidade_max(self):
        return self.capacidade_max
    def get_cobertura(self):
        return self.cobertura
    
    def set_n_identificacao(self, n_identificacao):
        self.n_identificacao = n_identificacao
    def set_esporte(self, esporte):
        self.esporte = esporte
    def set_valor_h(self, valor_h):
        self.valor_h = valor_h
    def set_capacidade_max(self, capacidade_max):
        self.capacidade_max = capacidade_max
    def set_cobertura(self, cobertura):
        self.cobertura = cobertura