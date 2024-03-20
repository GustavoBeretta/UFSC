class Automovel:
    def __init__(self, n_identificacao, modelo, valor_diaria):
        self.n_identificacao = n_identificacao
        self.modelo = modelo
        self.valor_diaria = valor_diaria

    def get_n_identificacao(self):
        return self.n_identificacao
    def get_modelo(self):
        return self.modelo
    def get_valor_diaria(self):
        return self.valor_diaria
    
    def set_n_identificacao(self, n_identificacao):
        self.n_identificacao = n_identificacao
    def set_modelo(self, modelo):
        self.modelo = modelo
    def set_valor_diaria(self, valor_diaria):
        self.valor_diaria = valor_diaria