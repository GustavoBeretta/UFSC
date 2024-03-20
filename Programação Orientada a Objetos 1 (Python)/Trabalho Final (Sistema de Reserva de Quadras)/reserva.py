class Reserva:
    def __init__(self, n_reserva, cpf, cliente, n_identificacao, quadra, ano, mes, dia, hora, duracao):
        self.n_reserva = n_reserva
        self.cpf = cpf
        self.cliente = cliente
        self.n_identificacao = n_identificacao
        self.quadra = quadra
        self.ano = ano
        self.mes = mes
        self.dia = dia
        self.hora = hora
        self.duracao = duracao
        self.valor = self.cliente.coeficiente_reserva() * self.quadra.get_valor_h() * self.duracao
        
    def get_n_reserva(self):
        return self.n_reserva
    def get_cpf(self):
        return self.cpf
    def get_n_identificacao(self):
        return self.n_identificacao
    def get_ano(self):
        return self.ano
    def get_mes(self):
        return self.mes
    def get_dia(self):
        return self.dia
    def get_hora(self):
        return self.hora
    def get_duracao(self):
        return self.duracao
    def get_valor(self):
        return self.valor

    def set_n_reserva(self, n_reserva):
        self.n_reserva = n_reserva
    def set_cpf(self, cpf, cliente):
        self.cpf = cpf
        self.cliente = cliente
        self.valor = self.cliente.coeficiente_reserva() * self.quadra.get_valor_h() * self.duracao
    def set_n_identificacao(self, n_identificacao, quadra):
        self.n_identificacao = n_identificacao
        self.quadra = quadra
        self.valor = self.cliente.coeficiente_reserva() * self.quadra.get_valor_h() * self.duracao
    def set_ano(self, ano):
        self.ano = ano
    def set_mes(self, mes):
        self.mes = mes
    def set_dia(self, dia):
        self.dia = dia
    def set_hora(self, hora):
        self.hora = hora
    def set_duracao(self, duracao):
        self.duracao = duracao
        self.valor = self.cliente.coeficiente_reserva() * self.quadra.get_valor_h() * self.duracao