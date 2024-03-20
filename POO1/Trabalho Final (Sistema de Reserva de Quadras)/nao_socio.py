from cliente import Cliente

class Nao_socio(Cliente):
    def __init__(self, cpf, nome, telefone):
        super().__init__(cpf, nome, telefone)
        self.tipo = 'Não-sócio'
        
    def get_tipo(self):
        return self.tipo