class Cliente:
    def __init__(self, cpf, nome, telefone):
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone

    def get_nome(self):
        return self.nome
    def get_cpf(self):
        return self.cpf
    def get_telefone(self):
        return self.telefone

    def set_nome (self, nome):
        self.nome = nome
    def set_cpf(self, cpf):
        self.cpf = cpf
    def set_telefone(self, telefone):
        self.telefone = telefone