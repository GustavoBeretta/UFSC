#classe Lista_clientes, que inicializa um dicionário que servirá como armazenamento dos clientes cadastrados
class Lista_clientes:
    def __init__(self):
        self.lista_clientes = {}
    
    def get_lista_clientes(self):
        return (self.lista_clientes)