from cliente import Cliente

class Socio(Cliente):
    def __init__(self, cpf, nome, telefone):
        super().__init__(cpf, nome, telefone)
        self.tipo = 'Sócio'
    
    def get_tipo(self):
        return self.tipo
    
    def coeficiente_reserva(self):
        return 0.75