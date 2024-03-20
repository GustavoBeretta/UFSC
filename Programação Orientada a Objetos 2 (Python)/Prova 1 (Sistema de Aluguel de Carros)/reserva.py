#classe Reserva, que une informações do cliente e do automóvel
class Reserva:
    def __init__(self, n_reserva, cpf, cliente, n_identificacao, automovel):
        self.n_reserva = n_reserva
        self.cpf = cpf
        self.cliente = cliente
        self.n_identificacao = n_identificacao
        self.automovel = automovel
        
    def get_n_reserva(self):
        return self.n_reserva
    def get_cpf(self):
        return self.cpf
    def get_n_identificacao(self):
        return self.n_identificacao